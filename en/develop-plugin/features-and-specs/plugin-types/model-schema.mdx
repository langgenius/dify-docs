---
dimensions:
  type:
    primary: reference
    detail: core
  level: intermediate
standard_title: Model Schema
language: en
title: Model API Interface
description: Comprehensive guide to the Dify model plugin API including implementation requirements for LLM, TextEmbedding, Rerank, Speech2text, and Text2speech models, with detailed specifications for all related data structures.
---

## Introduction

This document details the interfaces and data structures required to implement Dify model plugins. It serves as a technical reference for developers integrating AI models with the Dify platform.

<Note>
Before diving into this API reference, we recommend first reading the [Model Design Rules](/plugin-dev-en/0411-model-designing-rules) and [Model Plugin Introduction](/plugin-dev-en/0131-model-plugin-introduction) for conceptual understanding.
</Note>

<CardGroup cols={2}>
  <Card title="Provider Implementation" icon="plug" href="#model-provider">
    Learn how to implement model provider classes for different AI service providers
  </Card>
  <Card title="Model Types" icon="layer-group" href="#models">
    Implementation details for the five supported model types: LLM, Embedding, Rerank, Speech2Text, and Text2Speech
  </Card>
  <Card title="Data Structures" icon="database" href="#entities">
    Comprehensive reference for all data structures used in the model API
  </Card>
  <Card title="Error Handling" icon="triangle-exclamation" href="#common-interfaces">
    Guidelines for proper error mapping and exception handling
  </Card>
</CardGroup>

## Model Provider

Every model provider must inherit from the `__base.model_provider.ModelProvider` base class and implement the credential validation interface.

### Provider Credential Validation

<CodeGroup>
```python Core Implementation
def validate_provider_credentials(self, credentials: dict) -> None:
    """
    Validate provider credentials by making a test API call
    
    Parameters:
        credentials: Provider credentials as defined in `provider_credential_schema`
        
    Raises:
        CredentialsValidateFailedError: If validation fails
    """
    try:
        # Example implementation - validate using an LLM model instance
        model_instance = self.get_model_instance(ModelType.LLM)
        model_instance.validate_credentials(
            model="example-model", 
            credentials=credentials
        )
    except Exception as ex:
        logger.exception(f"Credential validation failed")
        raise CredentialsValidateFailedError(f"Invalid credentials: {str(ex)}")
```

```python Custom Model Provider
class XinferenceProvider(Provider):
    def validate_provider_credentials(self, credentials: dict) -> None:
        """
        For custom-only model providers, a simple implementation is sufficient
        as validation happens at the model level
        """
        pass
```
</CodeGroup>

<ParamField path="credentials" type="dict">
  Credential information as defined in the provider's YAML configuration under `provider_credential_schema`. 
  Typically includes fields like `api_key`, `organization_id`, etc.
</ParamField>

<Warning>
If validation fails, your implementation must raise a `CredentialsValidateFailedError` exception. This ensures proper error handling in the Dify UI.
</Warning>

<Tip>
For predefined model providers, you should implement a thorough validation method that verifies the credentials work with your API. For custom model providers (where each model has its own credentials), a simplified implementation is sufficient.
</Tip>

## Models

Dify supports five distinct model types, each requiring implementation of specific interfaces. However, all model types share some common requirements.

### Common Interfaces

Every model implementation, regardless of type, must implement these two fundamental methods:

#### 1. Model Credential Validation

<CodeGroup>
```python Implementation
def validate_credentials(self, model: str, credentials: dict) -> None:
    """
    Validate that the provided credentials work with the specified model
    
    Parameters:
        model: The specific model identifier (e.g., "gpt-4")
        credentials: Authentication details for the model
        
    Raises:
        CredentialsValidateFailedError: If validation fails
    """
    try:
        # Make a lightweight API call to verify credentials
        # Example: List available models or check account status
        response = self._api_client.validate_api_key(credentials["api_key"])
        
        # Verify the specific model is available if applicable
        if model not in response.get("available_models", []):
            raise CredentialsValidateFailedError(f"Model {model} is not available")
            
    except ApiException as e:
        raise CredentialsValidateFailedError(str(e))
```
</CodeGroup>

<ParamField path="model" type="string" required>
  The specific model identifier to validate (e.g., "gpt-4", "claude-3-opus")
</ParamField>

<ParamField path="credentials" type="dict" required>
  Credential information as defined in the provider's configuration
</ParamField>

#### 2. Error Mapping

<CodeGroup>
```python Implementation
@property
def _invoke_error_mapping(self) -> dict[type[InvokeError], list[type[Exception]]]:
    """
    Map provider-specific exceptions to standardized Dify error types
    
    Returns:
        Dictionary mapping Dify error types to lists of provider exception types
    """
    return {
        InvokeConnectionError: [
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            ConnectionRefusedError
        ],
        InvokeServerUnavailableError: [
            ServiceUnavailableError,
            HTTPStatusError
        ],
        InvokeRateLimitError: [
            RateLimitExceededError,
            QuotaExceededError
        ],
        InvokeAuthorizationError: [
            AuthenticationError,
            InvalidAPIKeyError,
            PermissionDeniedError
        ],
        InvokeBadRequestError: [
            InvalidRequestError,
            ValidationError
        ]
    }
```
</CodeGroup>

<Accordion title="Available Error Types">
  <ParamField path="InvokeConnectionError" type="class">
    Network connection failures, timeouts
  </ParamField>
  <ParamField path="InvokeServerUnavailableError" type="class">
    Service provider is down or unavailable
  </ParamField>
  <ParamField path="InvokeRateLimitError" type="class">
    Rate limits or quota limits reached
  </ParamField>
  <ParamField path="InvokeAuthorizationError" type="class">
    Authentication or permission issues
  </ParamField>
  <ParamField path="InvokeBadRequestError" type="class">
    Invalid parameters or requests
  </ParamField>
</Accordion>

<Tip>
You can alternatively raise these standardized error types directly in your code instead of relying on the error mapping. This approach gives you more control over error messages.
</Tip>

### LLM Implementation

To implement a Large Language Model provider, inherit from the `__base.large_language_model.LargeLanguageModel` base class and implement these methods:

#### 1. Model Invocation

This core method handles both streaming and non-streaming API calls to language models.

<CodeGroup>
```python Core Implementation
def _invoke(
    self, 
    model: str, 
    credentials: dict,
    prompt_messages: list[PromptMessage], 
    model_parameters: dict,
    tools: Optional[list[PromptMessageTool]] = None, 
    stop: Optional[list[str]] = None,
    stream: bool = True, 
    user: Optional[str] = None
) -> Union[LLMResult, Generator[LLMResultChunk, None, None]]:
    """
    Invoke the language model
    """
    # Prepare API parameters
    api_params = self._prepare_api_parameters(
        model, 
        credentials, 
        prompt_messages, 
        model_parameters,
        tools, 
        stop
    )
    
    try:
        # Choose between streaming and non-streaming implementation
        if stream:
            return self._invoke_stream(model, api_params, user)
        else:
            return self._invoke_sync(model, api_params, user)
            
    except Exception as e:
        # Map errors using the error mapping property
        self._handle_api_error(e)

# Helper methods for streaming and non-streaming calls
def _invoke_stream(self, model, api_params, user):
    # Implement streaming call and yield chunks
    pass
    
def _invoke_sync(self, model, api_params, user):
    # Implement synchronous call and return complete result
    pass
```
</CodeGroup>

<Accordion title="Parameters">
  <ParamField path="model" type="string" required>
    Model identifier (e.g., "gpt-4", "claude-3")
  </ParamField>
  
  <ParamField path="credentials" type="dict" required>
    Authentication credentials for the API
  </ParamField>
  
  <ParamField path="prompt_messages" type="list[PromptMessage]" required>
    Message list in Dify's standardized format:
    - For `completion` models: Include a single `UserPromptMessage`
    - For `chat` models: Include `SystemPromptMessage`, `UserPromptMessage`, `AssistantPromptMessage`, `ToolPromptMessage` as needed
  </ParamField>
  
  <ParamField path="model_parameters" type="dict" required>
    Model-specific parameters (temperature, top_p, etc.) as defined in the model's YAML configuration
  </ParamField>
  
  <ParamField path="tools" type="list[PromptMessageTool]">
    Tool definitions for function calling capabilities
  </ParamField>
  
  <ParamField path="stop" type="list[string]">
    Stop sequences that will halt model generation when encountered
  </ParamField>
  
  <ParamField path="stream" type="boolean" default={true}>
    Whether to return a streaming response
  </ParamField>
  
  <ParamField path="user" type="string">
    User identifier for API monitoring
  </ParamField>
</Accordion>

<Accordion title="Return Values">
  <ParamField path="stream=True" type="Generator[LLMResultChunk, None, None]">
    A generator yielding chunks of the response as they become available
  </ParamField>
  
  <ParamField path="stream=False" type="LLMResult">
    A complete response object with the full generated text
  </ParamField>
</Accordion>

<Tip>
We recommend implementing separate helper methods for streaming and non-streaming calls to keep your code organized and maintainable.
</Tip>

#### 2. Token Counting

<CodeGroup>
```python Implementation
def get_num_tokens(
    self, 
    model: str, 
    credentials: dict, 
    prompt_messages: list[PromptMessage],
    tools: Optional[list[PromptMessageTool]] = None
) -> int:
    """
    Calculate the number of tokens in the prompt
    """
    # Convert prompt_messages to the format expected by the tokenizer
    text = self._convert_messages_to_text(prompt_messages)
    
    try:
        # Use the appropriate tokenizer for this model
        tokenizer = self._get_tokenizer(model)
        return len(tokenizer.encode(text))
    except Exception:
        # Fall back to a generic tokenizer
        return self._get_num_tokens_by_gpt2(text)
```
</CodeGroup>

<Info>
If the model doesn't provide a tokenizer, you can use the base class's `_get_num_tokens_by_gpt2(text)` method for a reasonable approximation.
</Info>

#### 3. Custom Model Schema (Optional)

<CodeGroup>
```python Implementation
def get_customizable_model_schema(
    self, 
    model: str, 
    credentials: dict
) -> Optional[AIModelEntity]:
    """
    Get parameter schema for custom models
    """
    # For fine-tuned models, you might return the base model's schema
    if model.startswith("ft:"):
        base_model = self._extract_base_model(model)
        return self._get_predefined_model_schema(base_model)
    
    # For standard models, return None to use the predefined schema
    return None
```
</CodeGroup>

<Info>
This method is only necessary for providers that support custom models. It allows custom models to inherit parameter rules from base models.
</Info>

### TextEmbedding Implementation

<Info>
Text embedding models convert text into high-dimensional vectors that capture semantic meaning, which is useful for retrieval, similarity search, and classification.
</Info>

To implement a Text Embedding provider, inherit from the `__base.text_embedding_model.TextEmbeddingModel` base class:

#### 1. Core Embedding Method

<CodeGroup>
```python Implementation
def _invoke(
    self, 
    model: str, 
    credentials: dict,
    texts: list[str], 
    user: Optional[str] = None
) -> TextEmbeddingResult:
    """
    Generate embedding vectors for multiple texts
    """
    # Set up API client with credentials
    client = self._get_client(credentials)
    
    # Handle batching if needed
    batch_size = self._get_batch_size(model)
    all_embeddings = []
    total_tokens = 0
    start_time = time.time()
    
    # Process in batches to avoid API limits
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        
        # Make API call to the embeddings endpoint
        response = client.embeddings.create(
            model=model,
            input=batch,
            user=user
        )
        
        # Extract embeddings from response
        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)
        
        # Track token usage
        total_tokens += response.usage.total_tokens
    
    # Calculate usage metrics
    elapsed_time = time.time() - start_time
    usage = self._create_embedding_usage(
        model=model,
        tokens=total_tokens,
        latency=elapsed_time
    )
    
    return TextEmbeddingResult(
        model=model,
        embeddings=all_embeddings,
        usage=usage
    )
```
</CodeGroup>

<Accordion title="Parameters">
  <ParamField path="model" type="string" required>
    Embedding model identifier
  </ParamField>
  
  <ParamField path="credentials" type="dict" required>
    Authentication credentials for the embedding service
  </ParamField>
  
  <ParamField path="texts" type="list[string]" required>
    List of text inputs to embed
  </ParamField>
  
  <ParamField path="user" type="string">
    User identifier for API monitoring
  </ParamField>
</Accordion>

<Accordion title="Return Value">
  <ParamField path="TextEmbeddingResult" type="object" required>
    A structured response containing:
    - model: The model used for embedding
    - embeddings: List of embedding vectors corresponding to input texts
    - usage: Metadata about token usage and costs
  </ParamField>
</Accordion>

#### 2. Token Counting Method

<CodeGroup>
```python Implementation
def get_num_tokens(
    self, 
    model: str, 
    credentials: dict, 
    texts: list[str]
) -> int:
    """
    Calculate the number of tokens in the texts to be embedded
    """
    # Join all texts to estimate token count
    combined_text = " ".join(texts)
    
    try:
        # Use the appropriate tokenizer for this model
        tokenizer = self._get_tokenizer(model)
        return len(tokenizer.encode(combined_text))
    except Exception:
        # Fall back to a generic tokenizer
        return self._get_num_tokens_by_gpt2(combined_text)
```
</CodeGroup>

<Tip>
For embedding models, accurate token counting is important for cost estimation, but not critical for functionality. The `_get_num_tokens_by_gpt2` method provides a reasonable approximation for most models.
</Tip>

### Rerank Implementation

<Info>
Reranking models help improve search quality by re-ordering a set of candidate documents based on their relevance to a query, typically after an initial retrieval phase.
</Info>

To implement a Reranking provider, inherit from the `__base.rerank_model.RerankModel` base class:

<CodeGroup>
```python Implementation
def _invoke(
    self, 
    model: str, 
    credentials: dict,
    query: str, 
    docs: list[str], 
    score_threshold: Optional[float] = None, 
    top_n: Optional[int] = None,
    user: Optional[str] = None
) -> RerankResult:
    """
    Rerank documents based on relevance to the query
    """
    # Set up API client with credentials
    client = self._get_client(credentials)
    
    # Prepare request data
    request_data = {
        "query": query,
        "documents": docs,
    }
    
    # Call reranking API endpoint
    response = client.rerank(
        model=model,
        **request_data,
        user=user
    )
    
    # Process results
    ranked_results = []
    for i, result in enumerate(response.results):
        # Create RerankDocument for each result
        doc = RerankDocument(
            index=result.document_index,  # Original index in docs list
            text=docs[result.document_index],  # Original text
            score=result.relevance_score  # Relevance score
        )
        ranked_results.append(doc)
    
    # Sort by score in descending order
    ranked_results.sort(key=lambda x: x.score, reverse=True)
    
    # Apply score threshold filtering if specified
    if score_threshold is not None:
        ranked_results = [doc for doc in ranked_results if doc.score >= score_threshold]
    
    # Apply top_n limit if specified
    if top_n is not None and top_n > 0:
        ranked_results = ranked_results[:top_n]
    
    return RerankResult(
        model=model,
        docs=ranked_results
    )
```
</CodeGroup>

<Accordion title="Parameters">
  <ParamField path="model" type="string" required>
    Reranking model identifier
  </ParamField>
  
  <ParamField path="credentials" type="dict" required>
    Authentication credentials for the API
  </ParamField>
  
  <ParamField path="query" type="string" required>
    The search query text
  </ParamField>
  
  <ParamField path="docs" type="list[string]" required>
    List of document texts to be reranked
  </ParamField>
  
  <ParamField path="score_threshold" type="float">
    Optional minimum score threshold for filtering results
  </ParamField>
  
  <ParamField path="top_n" type="int">
    Optional limit on number of results to return
  </ParamField>
  
  <ParamField path="user" type="string">
    User identifier for API monitoring
  </ParamField>
</Accordion>

<Accordion title="Return Value">
  <ParamField path="RerankResult" type="object" required>
    A structured response containing:
    - model: The model used for reranking
    - docs: List of RerankDocument objects with index, text, and score
  </ParamField>
</Accordion>

<Warning>
Reranking can be computationally expensive, especially with large document sets. Implement batching for large document collections to avoid timeouts or excessive resource consumption.
</Warning>

### Speech2Text Implementation

<Info>
Speech-to-text models convert spoken language from audio files into written text, enabling applications like transcription services, voice commands, and accessibility features.
</Info>

To implement a Speech-to-Text provider, inherit from the `__base.speech2text_model.Speech2TextModel` base class:

<CodeGroup>
```python Implementation
def _invoke(
    self, 
    model: str, 
    credentials: dict,
    file: IO[bytes], 
    user: Optional[str] = None
) -> str:
    """
    Convert speech audio to text
    """
    # Set up API client with credentials
    client = self._get_client(credentials)
    
    try:
        # Determine the file format
        file_format = self._detect_audio_format(file)
        
        # Prepare the file for API submission
        # Most APIs require either a file path or binary data
        audio_data = file.read()
        
        # Call the speech-to-text API
        response = client.audio.transcriptions.create(
            model=model,
            file=("audio.mp3", audio_data),  # Adjust filename based on actual format
            user=user
        )
        
        # Extract and return the transcribed text
        return response.text
        
    except Exception as e:
        # Map to appropriate error type
        self._handle_api_error(e)
        
    finally:
        # Reset file pointer for potential reuse
        file.seek(0)
```

```python Helper Methods
def _detect_audio_format(self, file: IO[bytes]) -> str:
    """
    Detect the audio format based on file header
    """
    # Read the first few bytes to check the file signature
    header = file.read(12)
    file.seek(0)  # Reset file pointer
    
    # Check for common audio format signatures
    if header.startswith(b'RIFF') and header[8:12] == b'WAVE':
        return 'wav'
    elif header.startswith(b'ID3') or header.startswith(b'\xFF\xFB'):
        return 'mp3'
    elif header.startswith(b'OggS'):
        return 'ogg'
    elif header.startswith(b'fLaC'):
        return 'flac'
    else:
        # Default or additional format checks
        return 'mp3'  # Default assumption
```
</CodeGroup>

<Accordion title="Parameters">
  <ParamField path="model" type="string" required>
    Speech-to-text model identifier
  </ParamField>
  
  <ParamField path="credentials" type="dict" required>
    Authentication credentials for the API
  </ParamField>
  
  <ParamField path="file" type="IO[bytes]" required>
    Binary file object containing the audio to transcribe
  </ParamField>
  
  <ParamField path="user" type="string">
    User identifier for API monitoring
  </ParamField>
</Accordion>

<Accordion title="Return Value">
  <ParamField path="text" type="string" required>
    The transcribed text from the audio file
  </ParamField>
</Accordion>

<Tip>
Audio format detection is important for proper handling of different file types. Consider implementing a helper method to detect the format from the file header as shown in the example.
</Tip>

<Warning>
Some speech-to-text APIs have file size limitations. Consider implementing chunking for large audio files if necessary.
</Warning>

### Text2Speech Implementation

<Info>
Text-to-speech models convert written text into natural-sounding speech, enabling applications such as voice assistants, screen readers, and audio content generation.
</Info>

To implement a Text-to-Speech provider, inherit from the `__base.text2speech_model.Text2SpeechModel` base class:

<CodeGroup>
```python Implementation
def _invoke(
    self, 
    model: str, 
    credentials: dict, 
    content_text: str, 
    streaming: bool,
    user: Optional[str] = None
) -> Union[bytes, Generator[bytes, None, None]]:
    """
    Convert text to speech audio
    """
    # Set up API client with credentials
    client = self._get_client(credentials)
    
    # Get voice settings based on model
    voice = self._get_voice_for_model(model)
    
    try:
        # Choose implementation based on streaming preference
        if streaming:
            return self._stream_audio(
                client=client,
                model=model,
                text=content_text,
                voice=voice,
                user=user
            )
        else:
            return self._generate_complete_audio(
                client=client,
                model=model,
                text=content_text,
                voice=voice,
                user=user
            )
    except Exception as e:
        self._handle_api_error(e)
```

```python Helper Methods
def _stream_audio(self, client, model, text, voice, user=None):
    """
    Implementation for streaming audio output
    """
    # Make API request with stream=True
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        stream=True,
        user=user
    )
    
    # Yield chunks as they arrive
    for chunk in response:
        if chunk:
            yield chunk
            
def _generate_complete_audio(self, client, model, text, voice, user=None):
    """
    Implementation for complete audio file generation
    """
    # Make API request for complete audio
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        user=user
    )
    
    # Get audio data as bytes
    audio_data = response.content
    return audio_data
```
</CodeGroup>

<Accordion title="Parameters">
  <ParamField path="model" type="string" required>
    Text-to-speech model identifier
  </ParamField>
  
  <ParamField path="credentials" type="dict" required>
    Authentication credentials for the API
  </ParamField>
  
  <ParamField path="content_text" type="string" required>
    Text content to be converted to speech
  </ParamField>
  
  <ParamField path="streaming" type="boolean" required>
    Whether to return streaming audio or complete file
  </ParamField>
  
  <ParamField path="user" type="string">
    User identifier for API monitoring
  </ParamField>
</Accordion>

<Accordion title="Return Value">
  <ParamField path="streaming=True" type="Generator[bytes, None, None]">
    A generator yielding audio chunks as they become available
  </ParamField>
  
  <ParamField path="streaming=False" type="bytes">
    Complete audio data as bytes
  </ParamField>
</Accordion>

<Tip>
Most text-to-speech APIs require you to specify a voice along with the model. Consider implementing a mapping between Dify's model identifiers and the provider's voice options.
</Tip>

<Warning>
Long text inputs may need to be chunked for better speech synthesis quality. Consider implementing text preprocessing to handle punctuation, numbers, and special characters properly.
</Warning>


### Moderation Implementation

<Info>
Moderation models analyze content for potentially harmful, inappropriate, or unsafe material, helping maintain platform safety and content policies.
</Info>

To implement a Moderation provider, inherit from the `__base.moderation_model.ModerationModel` base class:

<CodeGroup>
```python Implementation
def _invoke(
    self, 
    model: str, 
    credentials: dict,
    text: str, 
    user: Optional[str] = None
) -> bool:
    """
    Analyze text for harmful content
    
    Returns:
        bool: False if the text is safe, True if it contains harmful content
    """
    # Set up API client with credentials
    client = self._get_client(credentials)
    
    try:
        # Call moderation API
        response = client.moderations.create(
            model=model,
            input=text,
            user=user
        )
        
        # Check if any categories were flagged
        result = response.results[0]
        
        # Return True if flagged in any category, False if safe
        return result.flagged
        
    except Exception as e:
        # Log the error but default to safe if there's an API issue
        # This is a conservative approach - production systems might want
        # different fallback behavior
        logger.error(f"Moderation API error: {str(e)}")
        return False
```

```python Detailed Implementation
def _invoke(
    self, 
    model: str, 
    credentials: dict,
    text: str, 
    user: Optional[str] = None
) -> bool:
    """
    Analyze text for harmful content with detailed category checking
    """
    # Set up API client with credentials
    client = self._get_client(credentials)
    
    try:
        # Call moderation API
        response = client.moderations.create(
            model=model,
            input=text,
            user=user
        )
        
        # Get detailed category results
        result = response.results[0]
        categories = result.categories
        
        # Check specific categories based on your application's needs
        # For example, you might want to flag certain categories but not others
        critical_violations = [
            categories.harassment,
            categories.hate,
            categories.self_harm,
            categories.sexual,
            categories.violence
        ]
        
        # Flag content if any critical category is violated
        return any(critical_violations)
        
    except Exception as e:
        self._handle_api_error(e)
        # Default to safe in case of error
        return False
```
</CodeGroup>

<Accordion title="Parameters">
  <ParamField path="model" type="string" required>
    Moderation model identifier
  </ParamField>
  
  <ParamField path="credentials" type="dict" required>
    Authentication credentials for the API
  </ParamField>
  
  <ParamField path="text" type="string" required>
    Text content to be analyzed
  </ParamField>
  
  <ParamField path="user" type="string">
    User identifier for API monitoring
  </ParamField>
</Accordion>

<Accordion title="Return Value">
  <ParamField path="result" type="boolean" required>
    Boolean indicating content safety:
    - False: The content is safe
    - True: The content contains harmful material
  </ParamField>
</Accordion>

<Warning>
Moderation is often used as a safety mechanism. Consider the implications of false negatives (letting harmful content through) versus false positives (blocking safe content) when implementing your solution.
</Warning>

<Tip>
Many moderation APIs provide detailed category scores rather than just a binary result. Consider extending this implementation to return more detailed information about specific categories of harmful content if your application needs it.
</Tip>

### Entities

#### PromptMessageRole

Message role

```python
class PromptMessageRole(Enum):
    """
    Enum class for prompt message.
    """
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
```

#### PromptMessageContentType

Message content type, divided into plain text and images.

```python
class PromptMessageContentType(Enum):
    """
    Enum class for prompt message content type.
    """
    TEXT = 'text'
    IMAGE = 'image'
```

#### PromptMessageContent

Message content base class, used only for parameter declaration, cannot be initialized.

```python
class PromptMessageContent(BaseModel):
    """
    Model class for prompt message content.
    """
    type: PromptMessageContentType
    data: str  # Content data
```

Currently supports two types: text and images, and can support text and multiple images simultaneously.
You need to initialize `TextPromptMessageContent` and `ImagePromptMessageContent` separately.

#### TextPromptMessageContent

```python
class TextPromptMessageContent(PromptMessageContent):
    """
    Model class for text prompt message content.
    """
    type: PromptMessageContentType = PromptMessageContentType.TEXT
```

When passing in text and images, text needs to be constructed as this entity as part of the `content` list.

#### ImagePromptMessageContent

```python
class ImagePromptMessageContent(PromptMessageContent):
    """
    Model class for image prompt message content.
    """
    class DETAIL(Enum):
        LOW = 'low'
        HIGH = 'high'

    type: PromptMessageContentType = PromptMessageContentType.IMAGE
    detail: DETAIL = DETAIL.LOW  # Resolution
```

When passing in text and images, images need to be constructed as this entity as part of the `content` list.
`data` can be a `url` or an image `base64` encoded string.

#### PromptMessage

Base class for all Role message bodies, used only for parameter declaration, cannot be initialized.

```python
class PromptMessage(ABC, BaseModel):
    """
    Model class for prompt message.
    """
    role: PromptMessageRole  # Message role
    content: Optional[str | list[PromptMessageContent]] = None  # Supports two types: string and content list. The content list is for multimodal needs, see PromptMessageContent for details.
    name: Optional[str] = None  # Name, optional.
```

#### UserPromptMessage

UserMessage message body, represents user messages.

```python
class UserPromptMessage(PromptMessage):
    """
    Model class for user prompt message.
    """
    role: PromptMessageRole = PromptMessageRole.USER
```

#### AssistantPromptMessage

Represents model response messages, typically used for `few-shots` or chat history input.

```python
class AssistantPromptMessage(PromptMessage):
    """
    Model class for assistant prompt message.
    """
    class ToolCall(BaseModel):
        """
        Model class for assistant prompt message tool call.
        """
        class ToolCallFunction(BaseModel):
            """
            Model class for assistant prompt message tool call function.
            """
            name: str  # Tool name
            arguments: str  # Tool parameters

        id: str  # Tool ID, only effective for OpenAI tool call, a unique ID for tool invocation, the same tool can be called multiple times
        type: str  # Default is function
        function: ToolCallFunction  # Tool call information

    role: PromptMessageRole = PromptMessageRole.ASSISTANT
    tool_calls: list[ToolCall] = []  # Model's tool call results (only returned when tools are passed in and the model decides to call them)
```

Here `tool_calls` is the list of `tool call` returned by the model after passing in `tools` to the model.

#### SystemPromptMessage

Represents system messages, typically used to set system instructions for the model.

```python
class SystemPromptMessage(PromptMessage):
    """
    Model class for system prompt message.
    """
    role: PromptMessageRole = PromptMessageRole.SYSTEM
```

#### ToolPromptMessage

Represents tool messages, used to pass results to the model for next-step planning after a tool has been executed.

```python
class ToolPromptMessage(PromptMessage):
    """
    Model class for tool prompt message.
    """
    role: PromptMessageRole = PromptMessageRole.TOOL
    tool_call_id: str  # Tool call ID, if OpenAI tool call is not supported, you can also pass in the tool name
```

The base class's `content` passes in the tool execution result.

#### PromptMessageTool

```python
class PromptMessageTool(BaseModel):
    """
    Model class for prompt message tool.
    """
    name: str  # Tool name
    description: str  # Tool description
    parameters: dict  # Tool parameters dict

```

***

#### LLMResult

```python
class LLMResult(BaseModel):
    """
    Model class for llm result.
    """
    model: str  # Actually used model
    prompt_messages: list[PromptMessage]  # Prompt message list
    message: AssistantPromptMessage  # Reply message
    usage: LLMUsage  # Tokens used and cost information
    system_fingerprint: Optional[str] = None  # Request fingerprint, refer to OpenAI parameter definition
```

#### LLMResultChunkDelta

Delta entity within each iteration in streaming response

```python
class LLMResultChunkDelta(BaseModel):
    """
    Model class for llm result chunk delta.
    """
    index: int  # Sequence number
    message: AssistantPromptMessage  # Reply message
    usage: Optional[LLMUsage] = None  # Tokens used and cost information, only returned in the last message
    finish_reason: Optional[str] = None  # Completion reason, only returned in the last message
```

#### LLMResultChunk

Iteration entity in streaming response

```python
class LLMResultChunk(BaseModel):
    """
    Model class for llm result chunk.
    """
    model: str  # Actually used model
    prompt_messages: list[PromptMessage]  # Prompt message list
    system_fingerprint: Optional[str] = None  # Request fingerprint, refer to OpenAI parameter definition
    delta: LLMResultChunkDelta  # Changes in content for each iteration
```

#### LLMUsage

```python
class LLMUsage(ModelUsage):
    """
    Model class for llm usage.
    """
    prompt_tokens: int  # Tokens used by prompt
    prompt_unit_price: Decimal  # Prompt unit price
    prompt_price_unit: Decimal  # Prompt price unit, i.e., unit price based on how many tokens
    prompt_price: Decimal  # Prompt cost
    completion_tokens: int  # Tokens used by completion
    completion_unit_price: Decimal  # Completion unit price
    completion_price_unit: Decimal  # Completion price unit, i.e., unit price based on how many tokens
    completion_price: Decimal  # Completion cost
    total_tokens: int  # Total tokens used
    total_price: Decimal  # Total cost
    currency: str  # Currency unit
    latency: float  # Request time (s)
```

***

#### TextEmbeddingResult

```python
class TextEmbeddingResult(BaseModel):
    """
    Model class for text embedding result.
    """
    model: str  # Actually used model
    embeddings: list[list[float]]  # Embedding vector list, corresponding to the input texts list
    usage: EmbeddingUsage  # Usage information
```

#### EmbeddingUsage

```python
class EmbeddingUsage(ModelUsage):
    """
    Model class for embedding usage.
    """
    tokens: int  # Tokens used
    total_tokens: int  # Total tokens used
    unit_price: Decimal  # Unit price
    price_unit: Decimal  # Price unit, i.e., unit price based on how many tokens
    total_price: Decimal  # Total cost
    currency: str  # Currency unit
    latency: float  # Request time (s)
```

***

#### RerankResult

```python
class RerankResult(BaseModel):
    """
    Model class for rerank result.
    """
    model: str  # Actually used model
    docs: list[RerankDocument]  # List of reranked segments        
```

#### RerankDocument

```python
class RerankDocument(BaseModel):
    """
    Model class for rerank document.
    """
    index: int  # Original sequence number
    text: str  # Segment text content
    score: float  # Score
```

## Related Resources

- [Model Design Rules](/plugin-dev-en/0411-model-designing-rules) - Understand the standards for model configuration
- [Model Plugin Introduction](/plugin-dev-en/0411-model-plugin-introduction) - Quickly understand the basic concepts of model plugins
- [Quickly Integrate a New Model](/plugin-dev-en/0211-getting-started-new-model) - Learn how to add new models to existing providers
- [Create a New Model Provider](/plugin-dev-en/0222-creating-new-model-provider) - Learn how to develop brand new model providers

{/*
Contributing Section
DO NOT edit this section!
It will be automatically generated by the script.
*/}

---

[Edit this page](https://github.com/langgenius/dify-docs/edit/main/plugin-dev-en/0412-model-schema.mdx) | [Report an issue](https://github.com/langgenius/dify-docs/issues/new?template=docs.yml)

