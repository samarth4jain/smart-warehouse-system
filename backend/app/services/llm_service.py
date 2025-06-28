import os
import torch
import logging
from typing import Optional, Dict, Any, List
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    BitsAndBytesConfig,
    pipeline
)
from huggingface_hub import login
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from pydantic import Field

logger = logging.getLogger(__name__)

class MultipleLLMService:
    """Smart LLM service that tries multiple approaches"""
    
    def __init__(self):
        self.llm = None
        self.service_type = None
        self._initialize_best_available_llm()
    
    def _initialize_best_available_llm(self):
        """Try different LLM approaches in order of preference"""
        
        # Method 1: Try Hugging Face Inference API (fastest to start)
        try:
            from .hf_inference_service import HFInferenceService
            logger.info("Attempting Hugging Face Inference API...")
            self.llm = HFInferenceService()
            self.service_type = "huggingface_inference"
            logger.info(" Successfully initialized Hugging Face Inference API")
            return
        except Exception as e:
            logger.warning(f"HF Inference API failed: {str(e)}")
        
        # Method 2: Try Ollama (good local option)
        try:
            from .ollama_service import OllamaService
            logger.info("Attempting Ollama local server...")
            self.llm = OllamaService()
            self.service_type = "ollama"
            logger.info(" Successfully initialized Ollama")
            return
        except Exception as e:
            logger.warning(f"Ollama failed: {str(e)}")
        
        # Method 3: Try smaller local model (lightweight)
        try:
            logger.info("Attempting lightweight local model...")
            self.llm = LightweightLocalLLM()
            self.service_type = "lightweight_local"
            logger.info(" Successfully initialized lightweight local model")
            return
        except Exception as e:
            logger.warning(f"Lightweight local model failed: {str(e)}")
        
        # Method 4: Try original Sheared LLaMA (if all else fails)
        try:
            logger.info("Attempting original Sheared LLaMA...")
            self.llm = ShearedLLaMALLM()
            self.service_type = "sheared_llama"
            logger.info(" Successfully initialized Sheared LLaMA")
            return
        except Exception as e:
            logger.warning(f"Sheared LLaMA failed: {str(e)}")
        
        # If all methods fail
        logger.error("All LLM initialization methods failed. Using mock service.")
        self.llm = MockLLMService()
        self.service_type = "mock"
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate response using available LLM"""
        if not self.llm:
            return "I apologize, but my AI capabilities are currently unavailable."
        
        try:
            return self.llm.generate_response(prompt, **kwargs)
        except Exception as e:
            logger.error(f"Error generating response with {self.service_type}: {str(e)}")
            return "I'm experiencing technical difficulties. Please try again."
    
    def is_available(self) -> bool:
        """Check if LLM service is available"""
        if not self.llm:
            return False
        
        try:
            return self.llm.is_available()
        except:
            return False
    
    def get_service_info(self) -> Dict[str, Any]:
        """Get information about current service"""
        return {
            "service_type": self.service_type,
            "available": self.is_available(),
            "model_name": getattr(self.llm, 'model_name', 'unknown')
        }

class LightweightLocalLLM:
    """Lightweight local model using smaller, faster models"""
    
    def __init__(self):
        self.model_name = "microsoft/DialoGPT-small"  # Much smaller and faster
        self.tokenizer = None
        self.model = None
        self.pipeline = None
        self._load_model()
    
    def _load_model(self):
        """Load lightweight model"""
        try:
            logger.info(f"Loading lightweight model: {self.model_name}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model (CPU only, no quantization)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True
            )
            
            # Create pipeline
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_new_tokens=256,
                temperature=0.7,
                do_sample=True,
                return_full_text=False
            )
            
            logger.info("Lightweight model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading lightweight model: {str(e)}")
            raise
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate response using lightweight model"""
        try:
            formatted_prompt = f"Human: {prompt}\nBot:"
            
            response = self.pipeline(
                formatted_prompt,
                max_new_tokens=kwargs.get('max_tokens', 256),
                temperature=kwargs.get('temperature', 0.7)
            )
            
            if response and len(response) > 0:
                return response[0]['generated_text'].strip()
            else:
                return "I'm having trouble generating a response."
                
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I apologize, but I'm having technical difficulties."
    
    def is_available(self) -> bool:
        """Check if model is available"""
        return self.pipeline is not None

class MockLLMService:
    """Mock service for when all else fails"""
    
    def __init__(self):
        self.model_name = "mock_llm"
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate mock intelligent responses"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['inventory', 'stock', 'products']):
            return "I can help you check inventory levels. Please use specific commands like 'check stock SKU: PROD001' for detailed information."
        
        elif any(word in prompt_lower for word in ['hello', 'hi', 'help']):
            return "Hello! I'm your warehouse assistant. I can help with inventory management, stock updates, and order processing. What would you like to do?"
        
        elif any(word in prompt_lower for word in ['order', 'dispatch', 'ship']):
            return "I can assist with order processing. Please provide order details or use commands like 'dispatch order ORD001'."
        
        else:
            return f"I understand you're asking about warehouse operations. While my advanced AI features are temporarily unavailable, I can still help with basic commands. Try asking about inventory, orders, or stock levels."
    
    def is_available(self) -> bool:
        """Mock service is always available"""
        return True

# Keep the original ShearedLLaMALLM as fallback
class ShearedLLaMALLM(LLM):
    """Custom LangChain LLM wrapper for conversational models like DialoGPT or Sheared LLaMA"""
    
    model_name: str = Field(default="princeton-nlp/Sheared-LLaMA-2.7B")
    device: str = Field(default="cpu")
    max_tokens: int = Field(default=256)
    temperature: float = Field(default=0.7)
    use_4bit: bool = Field(default=False)
    
    tokenizer: Optional[Any] = Field(default=None, exclude=True)
    model: Optional[Any] = Field(default=None, exclude=True)
    pipeline: Optional[Any] = Field(default=None, exclude=True)
    
    class Config:
        arbitrary_types_allowed = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._load_model()
    
    def _load_model(self):
        """Load the conversational model and tokenizer"""
        try:
            logger.info(f"Loading conversational model: {self.model_name}")
            
            # Authenticate with Hugging Face if token is provided
            hf_token = os.getenv("HUGGINGFACE_HUB_TOKEN")
            if hf_token:
                logger.info("Authenticating with Hugging Face Hub...")
                login(token=hf_token)
            
            # Check for GPU availability and configure accordingly
            has_gpu = torch.cuda.is_available()
            use_quantization = self.use_4bit and has_gpu
            
            if not has_gpu:
                logger.info("GPU not available - running on CPU")
                self.device = "cpu"
            
            # Configure quantization only if GPU is available and requested
            quantization_config = None
            model_dtype = torch.float32  # Better for CPU
            
            if use_quantization:
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.bfloat16
                )
                model_dtype = torch.bfloat16
                logger.info("Using 4-bit quantization with GPU")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True,
                padding_side="left"
            )
            
            # Add pad token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model with appropriate configuration
            model_kwargs = {
                "trust_remote_code": True,
                "low_cpu_mem_usage": True,
                "torch_dtype": model_dtype
            }
            
            if use_quantization:
                model_kwargs["quantization_config"] = quantization_config
                model_kwargs["device_map"] = self.device if self.device != "auto" else "auto"
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                **model_kwargs
            )
            
            # Ensure model is on correct device
            if self.device == "cpu":
                self.model = self.model.to("cpu")
            
            # Create pipeline
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_new_tokens=self.max_tokens,
                temperature=self.temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                return_full_text=False
            )
            
            logger.info("Conversational model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading conversational model: {str(e)}")
            raise
    
    @property
    def _llm_type(self) -> str:
        return "conversational_llm"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Run the LLM on the given prompt and input."""
        try:
            # Format prompt for chat-based model
            formatted_prompt = self._format_prompt(prompt)
            
            # Generate response
            response = self.pipeline(
                formatted_prompt,
                max_new_tokens=kwargs.get('max_tokens', self.max_tokens),
                temperature=kwargs.get('temperature', self.temperature),
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
            
            # Extract generated text
            generated_text = response[0]['generated_text'].strip()
            
            # Apply stop sequences if provided
            if stop:
                for stop_seq in stop:
                    if stop_seq in generated_text:
                        generated_text = generated_text.split(stop_seq)[0]
            
            return generated_text
            
        except Exception as e:
            logger.error(f"Error in LLM call: {str(e)}")
            return "I apologize, but I'm having trouble processing your request right now."
    
    def _format_prompt(self, prompt: str) -> str:
        """Format prompt for conversational model"""
        # For DialoGPT, we can use simple conversation format
        if "DialoGPT" in self.model_name:
            return f"Human: {prompt}\nBot:"
        # For Sheared LLaMA, use instruction format
        elif "Sheared-LLaMA" in self.model_name or "sheared" in self.model_name.lower():
            return f"### Instruction:\n{prompt}\n\n### Response:"
        # For other models, use a more generic format
        return f"User: {prompt}\nAssistant:"
    
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get the identifying parameters."""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "use_4bit": self.use_4bit,
        }


class LLMService:
    """Service to manage LLM operations"""
    
    def __init__(self):
        self.llm = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the LLM based on environment configuration"""
        try:
            model_name = os.getenv("LLM_MODEL_NAME", "princeton-nlp/Sheared-LLaMA-2.7B")
            device = os.getenv("LLM_DEVICE", "auto")
            max_tokens = int(os.getenv("LLM_MAX_TOKENS", "512"))
            temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
            use_4bit = os.getenv("LLM_USE_4BIT", "true").lower() == "true"
            
            self.llm = ShearedLLaMALLM(
                model_name=model_name,
                device=device,
                max_tokens=max_tokens,
                temperature=temperature,
                use_4bit=use_4bit
            )
            
            logger.info("LLM service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize LLM service: {str(e)}")
            raise
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate response using the LLM"""
        if not self.llm:
            raise RuntimeError("LLM not initialized")
        
        return self.llm(prompt, **kwargs)
    
    def is_available(self) -> bool:
        """Check if LLM is available"""
        return self.llm is not None
