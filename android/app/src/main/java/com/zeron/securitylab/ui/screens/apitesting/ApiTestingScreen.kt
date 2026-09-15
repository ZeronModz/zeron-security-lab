package com.zeron.securitylab.ui.screens.apitesting

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.zeron.securitylab.data.api.ApiRequestModel
import com.zeron.securitylab.data.repository.ZeronRepository
import com.zeron.securitylab.ui.theme.Error
import com.zeron.securitylab.ui.theme.OnBackground
import com.zeron.securitylab.ui.theme.OnSurface
import com.zeron.securitylab.ui.theme.OnSurfaceVariant
import com.zeron.securitylab.ui.theme.Primary
import com.zeron.securitylab.ui.theme.Surface
import com.zeron.securitylab.ui.theme.Success
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ApiTestingScreen() {
    var url by remember { mutableStateOf("") }
    var method by remember { mutableStateOf("GET") }
    var headers by remember { mutableStateOf("") }
    var body by remember { mutableStateOf("") }
    var authType by remember { mutableStateOf("None") }
    var authValue by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }
    var result by remember { mutableStateOf<Map<String, Any>?>(null) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var methodExpanded by remember { mutableStateOf(false) }
    var selectedTab by remember { mutableIntStateOf(0) }

    val scope = rememberCoroutineScope()
    val repository = remember { ZeronRepository() }
    val methods = listOf("GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS")
    val authTypes = listOf("None", "Bearer", "Basic", "API Key")

    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        item {
            Text(
                text = "API Testing",
                style = MaterialTheme.typography.headlineMedium,
                color = OnBackground,
                fontWeight = FontWeight.Bold,
            )
            Text(
                text = "Lightweight API client for testing endpoints",
                style = MaterialTheme.typography.bodyMedium,
                color = OnSurfaceVariant,
            )
        }

        item {
            Card(
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = Surface),
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    OutlinedTextField(
                        value = url,
                        onValueChange = { url = it },
                        label = { Text("Endpoint URL") },
                        placeholder = { Text("https://api.example.com/v1/resource") },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true,
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = Primary,
                            focusedLabelColor = Primary,
                        ),
                    )

                    Spacer(modifier = Modifier.height(12.dp))

                    ExposedDropdownMenuBox(
                        expanded = methodExpanded,
                        onExpandedChange = { methodExpanded = it },
                    ) {
                        OutlinedTextField(
                            value = method,
                            onValueChange = {},
                            readOnly = true,
                            label = { Text("Method") },
                            modifier = Modifier
                                .fillMaxWidth()
                                .menuAnchor(),
                            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = methodExpanded) },
                            colors = OutlinedTextFieldDefaults.colors(
                                focusedBorderColor = Primary,
                                focusedLabelColor = Primary,
                            ),
                        )
                        ExposedDropdownMenu(
                            expanded = methodExpanded,
                            onDismissRequest = { methodExpanded = false },
                        ) {
                            methods.forEach { m ->
                                DropdownMenuItem(
                                    text = { Text(m) },
                                    onClick = { method = m; methodExpanded = false },
                                )
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(12.dp))

                    TabRow(
                        selectedTabIndex = selectedTab,
                        containerColor = Surface,
                        contentColor = Primary,
                    ) {
                        Tab(selected = selectedTab == 0, onClick = { selectedTab = 0 }) {
                            Text("Headers", modifier = Modifier.padding(12.dp))
                        }
                        Tab(selected = selectedTab == 1, onClick = { selectedTab = 1 }) {
                            Text("Body", modifier = Modifier.padding(12.dp))
                        }
                        Tab(selected = selectedTab == 2, onClick = { selectedTab = 2 }) {
                            Text("Auth", modifier = Modifier.padding(12.dp))
                        }
                    }

                    when (selectedTab) {
                        0 -> {
                            OutlinedTextField(
                                value = headers,
                                onValueChange = { headers = it },
                                label = { Text("Headers (JSON)") },
                                placeholder = { Text("{\"Content-Type\": \"application/json\"}") },
                                modifier = Modifier.fillMaxWidth(),
                                minLines = 3,
                                colors = OutlinedTextFieldDefaults.colors(
                                    focusedBorderColor = Primary,
                                    focusedLabelColor = Primary,
                                ),
                            )
                        }
                        1 -> {
                            OutlinedTextField(
                                value = body,
                                onValueChange = { body = it },
                                label = { Text("Request Body") },
                                placeholder = { Text("{\"key\": \"value\"}") },
                                modifier = Modifier.fillMaxWidth(),
                                minLines = 5,
                                colors = OutlinedTextFieldDefaults.colors(
                                    focusedBorderColor = Primary,
                                    focusedLabelColor = Primary,
                                ),
                            )
                        }
                        2 -> {
                            Column {
                                authTypes.forEach { type ->
                                    Row(modifier = Modifier.fillMaxWidth()) {
                                        Text(
                                            text = type,
                                            color = if (authType == type) Primary else OnSurface,
                                            modifier = Modifier
                                                .weight(1f)
                                                .padding(vertical = 8.dp),
                                        )
                                    }
                                }
                                if (authType != "None") {
                                    OutlinedTextField(
                                        value = authValue,
                                        onValueChange = { authValue = it },
                                        label = { Text("Token / Key") },
                                        modifier = Modifier.fillMaxWidth(),
                                        singleLine = true,
                                        colors = OutlinedTextFieldDefaults.colors(
                                            focusedBorderColor = Primary,
                                            focusedLabelColor = Primary,
                                        ),
                                    )
                                }
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(16.dp))

                    Button(
                        onClick = {
                            scope.launch {
                                isLoading = true
                                errorMessage = null
                                result = null

                                val parsedHeaders = try {
                                    if (headers.isNotBlank()) {
                                        org.json.JSONObject(headers).let { obj ->
                                            obj.keys().asSequence().associateWith { obj.getString(it) }
                                        }
                                    } else emptyMap()
                                } catch (e: Exception) {
                                    emptyMap()
                                }

                                val effectiveAuthType = if (authType == "None") null else authType.lowercase()

                                repository.apiRequest(
                                    ApiRequestModel(
                                        url = url,
                                        method = method,
                                        headers = parsedHeaders,
                                        body = body.ifBlank { null },
                                        auth_type = effectiveAuthType,
                                        auth_value = authValue.ifBlank { null },
                                    )
                                ).fold(
                                    onSuccess = { result = it },
                                    onFailure = { errorMessage = it.message },
                                )
                                isLoading = false
                            }
                        },
                        modifier = Modifier.fillMaxWidth(),
                        enabled = url.isNotBlank() && !isLoading,
                        colors = ButtonDefaults.buttonColors(containerColor = Primary),
                        shape = RoundedCornerShape(12.dp),
                    ) {
                        if (isLoading) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(20.dp),
                                color = OnBackground,
                                strokeWidth = 2.dp,
                            )
                        } else {
                            Icon(Icons.Default.Send, contentDescription = null)
                            Spacer(modifier = Modifier.padding(4.dp))
                            Text("Send Request")
                        }
                    }
                }
            }
        }

        if (errorMessage != null) {
            item {
                Card(
                    shape = RoundedCornerShape(12.dp),
                    colors = CardDefaults.cardColors(containerColor = Error.copy(alpha = 0.1f)),
                ) {
                    Text(
                        text = errorMessage ?: "",
                        modifier = Modifier.padding(16.dp),
                        color = Error,
                    )
                }
            }
        }

        result?.let { data ->
            item {
                Card(
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = Surface),
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Response", color = OnBackground, fontWeight = FontWeight.SemiBold)
                        Spacer(modifier = Modifier.height(8.dp))

                        val statusCode = data["status_code"] as? Int ?: 0
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                        ) {
                            Text("Status", color = OnSurfaceVariant)
                            Text(
                                text = "$statusCode",
                                color = when {
                                    statusCode in 200..299 -> Success
                                    statusCode in 400..499 -> Error
                                    else -> Primary
                                },
                                fontWeight = FontWeight.Bold,
                            )
                        }

                        val responseTime = data["response_time_ms"] as? Int ?: 0
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                        ) {
                            Text("Response Time", color = OnSurfaceVariant)
                            Text("${responseTime}ms", color = OnSurface)
                        }

                        Spacer(modifier = Modifier.height(12.dp))
                        Text("Body", color = OnSurface, fontWeight = FontWeight.Medium)
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            text = (data["body"] as? String)?.take(3000) ?: data.toString().take(3000),
                            color = OnSurfaceVariant,
                            style = MaterialTheme.typography.bodySmall,
                        )
                    }
                }
            }
        }
    }
}
