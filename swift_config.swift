// GoogleCloudConfig.swift
// Configuration for connecting to the Veo proxy server

import Foundation

struct GoogleCloudConfig {
    // Update this to your proxy server URL
    // For local development: "http://localhost:5000"
    // For production: Replace with your deployed server URL
    static let baseURL = "http://localhost:5000"
    
    // These values match your proxy server configuration
    static let projectId = "daring-runway-465515-i2"
    static let region = "us-central1"
    
    enum VeoModel: String {
        case veo2 = "veo-2.0-generate-001"
        case veo3 = "veo-3.0-generate-preview"
        case veo3Fast = "veo-3.0-fast-generate-001"
    }
}

// Update your VeoAPIService to use the proxy endpoints
extension VeoAPIService {
    // Override the performRequest method to use simplified endpoints
    private func performRequestViaProxy<T: Decodable, B: Encodable>(
        endpoint: String,
        method: String,
        body: B? = nil
    ) async throws -> T {
        // For predictLongRunning, use the simplified endpoint
        if endpoint.contains(":predictLongRunning") {
            return try await performSimplifiedRequest(body: body)
        }
        
        // For fetchPredictOperation, use the simplified check endpoint
        if endpoint.contains(":fetchPredictOperation") {
            return try await performCheckOperation(body: body)
        }
        
        // Default behavior for other endpoints
        guard let url = URL(string: GoogleCloudConfig.baseURL + endpoint) else {
            throw VeoError(error: "Invalid URL", message: "Failed to construct URL")
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        if let body = body {
            request.httpBody = try JSONEncoder().encode(body)
        }
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw VeoError(error: "Invalid response", message: "Failed to get HTTP response")
        }
        
        if httpResponse.statusCode == 200 {
            return try JSONDecoder().decode(T.self, from: data)
        } else {
            let errorMessage = String(data: data, encoding: .utf8) ?? "Unknown error"
            throw VeoError(
                error: "HTTP Error",
                message: "Status code: \(httpResponse.statusCode) - \(errorMessage)"
            )
        }
    }
    
    private func performSimplifiedRequest<T: Decodable, B: Encodable>(body: B?) async throws -> T {
        guard let url = URL(string: GoogleCloudConfig.baseURL + "/generate-video") else {
            throw VeoError(error: "Invalid URL", message: "Failed to construct URL")
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        // Convert the Veo request to simplified format
        if let veoRequest = body as? VeoVideoGenerationRequest {
            var simplifiedBody: [String: Any] = [:]
            
            if let instance = veoRequest.instances.first {
                if let prompt = instance.prompt {
                    simplifiedBody["prompt"] = prompt
                }
                
                if let image = instance.image {
                    if let base64 = image.bytesBase64Encoded {
                        simplifiedBody["image"] = base64
                        simplifiedBody["imageMimeType"] = image.mimeType
                    }
                }
            }
            
            if let params = veoRequest.parameters {
                simplifiedBody["aspectRatio"] = params.aspectRatio
                simplifiedBody["durationSeconds"] = params.durationSeconds
                simplifiedBody["enhancePrompt"] = params.enhancePrompt
                simplifiedBody["generateAudio"] = params.generateAudio
                simplifiedBody["personGeneration"] = params.personGeneration
                simplifiedBody["sampleCount"] = params.sampleCount
                
                if let negativePrompt = params.negativePrompt {
                    simplifiedBody["negativePrompt"] = negativePrompt
                }
                if let seed = params.seed {
                    simplifiedBody["seed"] = seed
                }
                if let storageUri = params.storageUri {
                    simplifiedBody["storageUri"] = storageUri
                }
            }
            
            request.httpBody = try JSONSerialization.data(withJSONObject: simplifiedBody)
        }
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw VeoError(error: "Invalid response", message: "Failed to get HTTP response")
        }
        
        if httpResponse.statusCode == 200 {
            return try JSONDecoder().decode(T.self, from: data)
        } else {
            let errorMessage = String(data: data, encoding: .utf8) ?? "Unknown error"
            throw VeoError(
                error: "HTTP Error",
                message: "Status code: \(httpResponse.statusCode) - \(errorMessage)"
            )
        }
    }
    
    private func performCheckOperation<T: Decodable, B: Encodable>(body: B?) async throws -> T {
        guard let url = URL(string: GoogleCloudConfig.baseURL + "/check-operation") else {
            throw VeoError(error: "Invalid URL", message: "Failed to construct URL")
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        if let body = body {
            request.httpBody = try JSONEncoder().encode(body)
        }
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw VeoError(error: "Invalid response", message: "Failed to get HTTP response")
        }
        
        if httpResponse.statusCode == 200 {
            return try JSONDecoder().decode(T.self, from: data)
        } else {
            let errorMessage = String(data: data, encoding: .utf8) ?? "Unknown error"
            throw VeoError(
                error: "HTTP Error",
                message: "Status code: \(httpResponse.statusCode) - \(errorMessage)"
            )
        }
    }
}