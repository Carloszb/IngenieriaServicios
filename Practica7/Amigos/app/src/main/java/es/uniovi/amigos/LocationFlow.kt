package es.uniovi.amigos

import android.annotation.SuppressLint
import android.content.Context
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import androidx.core.content.ContextCompat
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow
import kotlinx.coroutines.flow.flowOf

sealed class LocationResult {
    data class NewLocation(val location: Location) : LocationResult()
    object PermissionDenied : LocationResult()
    object ProviderDisabled : LocationResult()
}

@SuppressLint("MissingPermission")
fun Context.createLocationFlow(): Flow<LocationResult> {
    val hasFine = ContextCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED
    val hasCoarse = ContextCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED
    if (!hasFine && !hasCoarse) {
        return flowOf(LocationResult.PermissionDenied)
    }

    val locationManager = getSystemService(Context.LOCATION_SERVICE) as LocationManager

    val isGpsEnabled = locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER)
    if (!isGpsEnabled) {
        return flowOf(LocationResult.ProviderDisabled)
    }

    return callbackFlow {
        val locationListener = object : LocationListener {
            override fun onLocationChanged(location: Location) {
                trySend(LocationResult.NewLocation(location))
            }

            override fun onProviderDisabled(provider: String) {
                trySend(LocationResult.ProviderDisabled)
            }
        }

        try {
            locationManager.requestLocationUpdates(
                LocationManager.GPS_PROVIDER,
                5000L,
                10f,
                locationListener
            )
        } catch (se: SecurityException) {
            trySend(LocationResult.PermissionDenied)
            close(se)
        }

        awaitClose {
            locationManager.removeUpdates(locationListener)
        }
    }
}