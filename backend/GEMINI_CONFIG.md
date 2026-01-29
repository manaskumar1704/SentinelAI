# Google Gemini Model Configuration Guide

## Available Models

### Recommended: Gemini 2.0 Flash (Experimental)

- **Model ID**: `gemini-2.0-flash-exp`
- **Best for**: Fast responses, cost-effective, general-purpose AI tasks
- **Context Window**: 1M tokens
- **Use cases**:
  - AI Counsellor chat
  - University classification
  - Quick recommendations

### Alternative: Gemini 1.5 Pro

- **Model ID**: `gemini-1.5-pro`
- **Best for**: Complex reasoning, longer context
- **Context Window**: 2M tokens
- **Use cases**:
  - Deep analysis of student profiles
  - Complex multi-university comparisons
  - Long conversation histories

### Alternative: Gemini 1.5 Flash

- **Model ID**: `gemini-1.5-flash`
- **Best for**: Balanced speed and capability
- **Context Window**: 1M tokens
- **Use cases**:
  - Standard AI counselling
  - Real-time interactions

## How to Change Models

### Global Default

Edit the default model parameter in these files:

1. **`services/gemini_client.py`**:

   ```python
   async def chat_with_counsellor(
       messages: list[dict],
       user_context: Optional[dict] = None,
       model: str = "gemini-2.0-flash-exp"  # Change here
   ) -> str:
   ```

2. **`ai_engine/rag_pipeline.py`**:

   ```python
   async def classify_university_with_ai(
       student_profile: dict,
       university_data: dict,
       model: str = "gemini-2.0-flash-exp"  # Change here
   ) -> dict:
   ```

3. **`ai_engine/client.py`**:

   ```python
   async def generate_response(
       messages: list[dict],
       temperature: float = 0.7,
       max_tokens: int = 1024,
       model: str = "gemini-2.0-flash-exp"  # Change here
   ) -> str:
   ```

### Per-Function Override

You can also pass the model parameter when calling functions:

```python
# Use Gemini 1.5 Pro for this specific call
response = await chat_with_counsellor(
    messages=messages,
    user_context=context,
    model="gemini-1.5-pro"
)
```

## Temperature Settings

### Current Settings

- **Classification**: `temperature=0.3` (more deterministic)
- **Explanations**: `temperature=0.7` (more creative)
- **Chat**: `temperature=0.7` (balanced)

### Adjustment Guidelines

- **Lower (0.0-0.3)**: More consistent, factual responses
- **Medium (0.4-0.7)**: Balanced creativity and consistency
- **Higher (0.8-1.0)**: More creative, varied responses

## Token Limits

### Current Settings

- **Classification**: 512 tokens
- **Explanations**: 512 tokens
- **Chat**: 1024 tokens

### When to Adjust

- Increase if responses are getting cut off
- Decrease to reduce costs and latency

## Cost Optimization

### Tips

1. Use Gemini 2.0 Flash for most operations (cheapest)
2. Reserve Gemini 1.5 Pro for complex analysis only
3. Keep token limits as low as practical
4. Use lower temperature for classification (faster, cheaper)

## Performance Tuning

### For Faster Responses

- Use `gemini-2.0-flash-exp`
- Lower `max_output_tokens`
- Lower `temperature`

### For Better Quality

- Use `gemini-1.5-pro`
- Higher `max_output_tokens`
- Moderate `temperature` (0.7)

### For Cost Efficiency

- Use `gemini-2.0-flash-exp`
- Minimize `max_output_tokens`
- Batch operations when possible

## Monitoring

### Check API Usage

Visit [Google Cloud Console](https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com) to monitor:

- Request counts
- Token usage
- Error rates
- Costs

## Troubleshooting

### Common Issues

1. **"API key not set" error**
   - Ensure `GOOGLE_API_KEY` is in your `.env` file
   - Restart the server after adding the key

2. **Rate limit errors**
   - Reduce concurrent requests
   - Add retry logic with exponential backoff
   - Upgrade to higher quota tier

3. **Response quality issues**
   - Try different models
   - Adjust temperature
   - Improve prompt engineering

4. **Slow responses**
   - Switch to Gemini 2.0 Flash
   - Reduce max_output_tokens
   - Check network latency

## Model Comparison

| Feature | Gemini 2.0 Flash | Gemini 1.5 Flash | Gemini 1.5 Pro |
|---------|------------------|------------------|----------------|
| Speed | ⚡⚡⚡ Fastest | ⚡⚡ Fast | ⚡ Moderate |
| Cost | 💰 Lowest | 💰💰 Low | 💰💰💰 Higher |
| Quality | ✅ Good | ✅✅ Better | ✅✅✅ Best |
| Context | 1M tokens | 1M tokens | 2M tokens |
| Best for | Chat, Quick tasks | General purpose | Complex analysis |

## Recommended Configuration by Use Case

### AI Counsellor Chat

```python
model = "gemini-2.0-flash-exp"
temperature = 0.7
max_tokens = 1024
```

### University Classification

```python
model = "gemini-2.0-flash-exp"
temperature = 0.3
max_tokens = 512
```

### Detailed Analysis

```python
model = "gemini-1.5-pro"
temperature = 0.5
max_tokens = 2048
```

### Batch Processing

```python
model = "gemini-2.0-flash-exp"
temperature = 0.3
max_tokens = 256
```
