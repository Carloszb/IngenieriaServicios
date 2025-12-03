package es.uniovi.converter

import android.os.Bundle
import android.view.View
import android.widget.EditText
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

class MainActivity : AppCompatActivity() {
    private var euroToDollar: Double = 1.16
    private lateinit var editTextEuros: EditText
    private lateinit var editTextDollars: EditText

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)

        editTextEuros = findViewById(R.id.editTextEuros)
        editTextDollars = findViewById(R.id.editTextDollars)

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
    }

    private fun convert(source: EditText, destination: EditText, factor: Double) {
        val text = source.text.toString()
        val value = text.toDoubleOrNull()
        if (value == null) {
            destination.setText("")
            return
        }
        destination.setText((value * factor).toString())
    }

    fun onClickToDollars(view: View) {
        convert(editTextEuros, editTextDollars, euroToDollar)
    }

    fun onClickToEuros(view: View) {
        convert(editTextDollars, editTextEuros, 1 / euroToDollar)
    }
}