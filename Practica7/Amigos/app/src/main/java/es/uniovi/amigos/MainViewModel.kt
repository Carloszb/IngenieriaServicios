package es.uniovi.amigos

import android.app.Application
import android.util.Log
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import com.google.firebase.messaging.FirebaseMessaging
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch
import kotlinx.coroutines.tasks.await

class MainViewModel(application: Application) : AndroidViewModel(application) {

    private val locationFlow = application.createLocationFlow()

    val amigosList = MutableLiveData<List<Amigo>>()
    var userName: String? = null
    var userId: Int? = null

    private var locationJob: Job? = null

    init {
        getAmigosList()
    }

    fun getAmigosList() {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.api.getAmigos()
                if (response.isSuccessful) {
                    amigosList.postValue(response.body())
                    Log.d("MainViewModel", "Lista de amigos actualizada")
                }
            } catch (e: Exception) {
                Log.e("MainViewModel", "Error al obtener amigos: ${e.message}")
            }
        }
    }

    fun registerUserName(name: String) {
        userName = name
        Log.d("MainViewModel", "Nombre de usuario establecido: $userName")
        viewModelScope.launch {
            try {
                val response = RetrofitClient.api.getAmigoByName(name)
                if (response.isSuccessful) {
                    val amigo = response.body()
                    userId = amigo?.id
                    Log.d("MainViewModel", "ID recuperado: $userId")

                    val token = FirebaseMessaging.getInstance().token.await()
                    Log.d("MainViewModel", "Usuario: $userName, Id: $userId, Token: $token")

                    if (userId != null) {
                        val payload = AmigosApiService.DeviceTokenPayload(token)
                        val tokenResponse = RetrofitClient.api.updateAmigoDeviceToken(userId!!, payload)
                        if (tokenResponse.isSuccessful) {
                            Log.d("MainViewModel", "Token enviado al servidor correctamente")
                        } else {
                            Log.e("MainViewModel", "Error enviando token: ${tokenResponse.code()}")
                        }
                    }

                } else {
                    Log.e("MainViewModel", "Error API: ${response.code()}")
                }
            } catch (e: Exception) {
                Log.e("MainViewModel", "Error red: ${e.message}")
            }
        }
    }

    fun startLocationUpdates() {
        if (locationJob?.isActive == true) return

        locationJob = viewModelScope.launch {
            locationFlow.collect { result ->
                if (result is LocationResult.NewLocation) {
                    val location = result.location

                    userId?.let { idNoNulo ->
                        try {
                            val payload = AmigosApiService.LocationPayload(
                                lati = location.latitude,
                                longi = location.longitude
                            )
                            RetrofitClient.api.updateAmigoPosition(idNoNulo, payload)
                        } catch (e: Exception) {
                            Log.e("API_PUT", "Fallo de red: ${e.message}")
                        }
                    }

                } else if (result is LocationResult.PermissionDenied) {
                    Log.w("Location", "Permiso de ubicación denegado")
                } else if (result is LocationResult.ProviderDisabled) {
                    Log.w("Location", "Proveedor GPS desactivado")
                }
            }
        }
    }
}