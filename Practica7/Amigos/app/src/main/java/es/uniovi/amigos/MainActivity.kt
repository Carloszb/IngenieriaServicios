package es.uniovi.amigos

import android.Manifest
import android.app.AlertDialog
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.os.Bundle
import android.util.Log
import android.widget.EditText
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.lifecycle.lifecycleScope
import androidx.preference.PreferenceManager
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.osmdroid.config.Configuration
import org.osmdroid.tileprovider.tilesource.TileSourceFactory
import org.osmdroid.util.GeoPoint
import org.osmdroid.views.MapView
import org.osmdroid.views.overlay.Marker

class MainActivity : AppCompatActivity() {
    private var map: MapView? = null
    private val viewModel: MainViewModel by viewModels()

    private val updateReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            if (intent?.action == "updateFromServer") {
                Log.d("MainActivity", "¡Aviso de FCM recibido! Actualizando lista...")
                viewModel.getAmigosList()
            }
        }
    }

    private val requestPermissionLauncher =
        registerForActivityResult(
            ActivityResultContracts.RequestMultiplePermissions()
        ) { permissions ->
            if (permissions[Manifest.permission.ACCESS_FINE_LOCATION] == true) {
                viewModel.startLocationUpdates()
            }
        }

    private fun checkAndRequestLocationPermissions() {
        val permissionsToRequest = arrayOf(
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION
        )

        if (permissionsToRequest.all
            { ContextCompat.checkSelfPermission(this, it) == PackageManager.PERMISSION_GRANTED }
        ) {
            viewModel.startLocationUpdates()
        } else {
            requestPermissionLauncher.launch(permissionsToRequest)
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val ctx: Context = applicationContext
        Configuration.getInstance().load(ctx, PreferenceManager.getDefaultSharedPreferences(ctx))

        setContentView(R.layout.activity_main)

        map = findViewById(R.id.map)
        map?.setTileSource(TileSourceFactory.MAPNIK)
        map?.setLayerType(android.view.View.LAYER_TYPE_SOFTWARE, null)

        lifecycleScope.launch {
            withContext(Dispatchers.Main) {
                centrarMapaEnEuropa()
            }
        }

        viewModel.amigosList.observe(this@MainActivity) { listaDeAmigos ->
            if (listaDeAmigos != null) {
                paintAmigosList(listaDeAmigos)
            }
        }
        checkAndRequestLocationPermissions()

        if (viewModel.userName == null) {
            askUserName()
        }
    }

    private fun askUserName() {
        val builder = AlertDialog.Builder(this)
        builder.setTitle("Identificación")
        builder.setMessage("Introduce tu nombre de usuario:")
        val input = EditText(this)
        builder.setView(input)
        builder.setPositiveButton("Aceptar") { _, _ ->
            val name = input.text.toString()
            if (name.isNotBlank()) {
                viewModel.registerUserName(name)
            }
        }
        builder.setCancelable(false)
        builder.show()
    }

    fun centrarMapaEnEuropa() {
        val mapController = map?.controller
        mapController?.setZoom(5.5)
        val startPoint = GeoPoint(48.8583, 2.2944)
        mapController?.setCenter(startPoint)
    }

    override fun onResume() {
        super.onResume()
        map?.onResume()
        val filter = IntentFilter("updateFromServer")
        registerReceiver(updateReceiver, filter, Context.RECEIVER_NOT_EXPORTED)
    }

    override fun onPause() {
        super.onPause()
        map?.onPause()
        unregisterReceiver(updateReceiver)
    }

    private fun addMarker(lat: Double, lon: Double, title: String?) {
        map?.let { mapaNoNulo ->
            val marker = Marker(mapaNoNulo)
            marker.position = GeoPoint(lat, lon)
            marker.setAnchor(Marker.ANCHOR_CENTER, Marker.ANCHOR_BOTTOM)
            marker.title = title ?: "Desconocido"
            mapaNoNulo.overlays.add(marker)
        }
    }

    private fun paintAmigosList(amigos: List<Amigo>) {
        map?.overlays?.clear()
        for (amigo in amigos) {
            addMarker(amigo.lati, amigo.longi, amigo.name)
        }
        map?.invalidate()
    }
}