package es.uniovi.converter

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch

class MainViewModel : ViewModel() {
    var euroToDollar: Double = 1.16

    fun fetchExchangeRate() {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.api.convert("EUR", "USD", 1.0)
                val exchangeRateResponse = response.body()
                if (!response.isSuccessful || exchangeRateResponse == null) {
                    Log.e("MainViewModel", "Error al obtener el cambio: ${response.code()}")
                    return@launch
                }
                euroToDollar = exchangeRateResponse.rates.USD
                Log.d("MainViewModel", "Cambio actualizado: $euroToDollar")
            } catch (e: Exception) {
                Log.e("MainViewModel", "Excepción al obtener el cambio", e)
            }
        }
    }
}