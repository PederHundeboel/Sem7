package com.example.draughtapp.ApiClasses

import retrofit2.http.GET
import retrofit2.http.Path

interface Api {

    @GET("api/android/{lat}/{long}")
    suspend fun getLatLong(
        @Path("lat") lat: Double,
        @Path("long") long: Double,
    ): GridAsString
}