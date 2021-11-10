package com.example.draughtapp.ApiClasses

class Repository {
    suspend fun getLatLong(lat: Double, long: Double): GridAsString{
        return RetrofitInstance.api.getLatLong(lat, long)
    }

}