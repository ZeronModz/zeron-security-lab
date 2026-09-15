# Add project specific ProGuard rules here.
-keepattributes Signature
-keepattributes *Annotation*
-keep class com.zeron.securitylab.data.api.** { *; }
-keep class com.zeron.securitylab.domain.model.** { *; }
-dontwarn okhttp3.**
-dontwarn retrofit2.**
