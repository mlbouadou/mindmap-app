plugins {
    id("com.android.application") version "8.9.2"
    id("org.jetbrains.kotlin.android") version "2.2.10"
}

android {
    namespace = "com.example.mindmap"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.example.mindmap"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "0.1"
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    sourceSets.getByName("main") {
        manifest.srcFile("studio/AndroidManifest.xml")
        java.setSrcDirs(emptyList<String>())
    }
}

kotlin {
    jvmToolchain(17)

    sourceSets.getByName("main").kotlin.apply {
        setSrcDirs(listOf("studio"))
        include("MainActivity.kt")
    }
}
