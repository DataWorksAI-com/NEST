from typing import Callable
from a2a.types import TextPart 
from a2a.utils import new_agent_text_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue

class NANDAAgentExecutor(AgentExecutor):
    """Agent executor that delegates to NANDA bridge handler"""
    
    def __init__(self, message_handler: Callable):
        self.message_handler = message_handler
    
    async def execute(self, context: RequestContext, event_queue: EventQueue):
        """Execute agent logic via bridge handler"""
        try:
            # Extract message text from context
            message_text = ""
            if context.message and context.message.parts:
                for part in context.message.parts:
                    # Handle different part types
                    if hasattr(part, 'root'):
                        part_obj = part.root
                    else:
                        part_obj = part
                    
                    # Extract text based on part type
                    if hasattr(part_obj, 'text'):
                        message_text = part_obj.text
                    elif hasattr(part_obj, 'kind') and part_obj.kind == 'text':
                        message_text = part_obj.text if hasattr(part_obj, 'text') else str(part_obj)
                    else:
                        message_text = str(part_obj)
                    
                    if message_text:
                        break
            
            if not message_text:
                message_text = ""
            
            print(f"📨 Received message: {message_text[:100]}")
            
            # Convert to bridge format
            bridge_message = {
                "content": {
                    "text": message_text,
                    "type": "text"
                },
                "conversation_id": context.task_id or context.context_id or ""
            }
            
            # Call bridge handler
            response = await self.message_handler(bridge_message)
            
            # Extract response text
            response_text = response.get("content", {}).get("text", "")
            
            print(f"✅ Sending response: {response_text}")
            
            # Send response via event queue
            response_message = new_agent_text_message(response_text)
            await event_queue.enqueue_event(response_message)
            
        except Exception as e:
            print(f"❌ Error in execute: {e}")
            import traceback
            traceback.print_exc()
            # Send error message
            error_message = new_agent_text_message(f"Error: {str(e)}")
            event_queue.enqueue_event(error_message)
    
    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        """Handle task cancellation"""
        event_queue.enqueue_event(new_agent_text_message("Task cancelled"))
