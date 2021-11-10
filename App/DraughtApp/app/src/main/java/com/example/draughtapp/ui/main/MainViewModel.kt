package com.example.draughtapp.ui.main

import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.draughtapp.ApiClasses.GridAsString
import com.example.draughtapp.ApiClasses.Repository
import kotlinx.coroutines.launch

class MainViewModel(private val Repository: Repository) : ViewModel() {

    val response: MutableLiveData<GridAsString> = MutableLiveData()

    fun getLatLong(lat: Double, long: Double){
        viewModelScope.launch {
            val res = Repository.getLatLong(lat, long)
            response.value = res
        }
    }
}