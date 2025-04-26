import httpx
from azure.servicebus.aio import ServiceBusClient
from src.config import Config


class NotificationConsumer:
    def __init__(self):
        self.connection_string = Config.AZURE_SERVICE_BUS_CONNECTION_STRING
        self.queue_name = Config.AZURE_SERVICE_BUS_QUEUE_NAME
        self.webhook_url = Config.WEBHOOK_URL

    async def process_messages(self):
        async with ServiceBusClient.from_connection_string(self.connection_string) as client:
            receiver = client.get_queue_receiver(queue_name=self.queue_name)
            async with receiver:
                print("Listening for messages...")
                async for message in receiver:
                    try:
                        # 1. decode the message body
                        body = ''.join(  # message isinstance(message.body, (list, Generator)
                            part.decode('utf-8') if isinstance(part, bytes) else str(part) for part in message.body)

                        print(f"Received message: {body}")
                        book_title, review_content = body.split('|')

                        # 2. invoke the webhook
                        await self.invoke_webhook(book_title, review_content)

                        # 3. mark the message as completed
                        await receiver.complete_message(message)
                        print("Message completed and removed from the queue.")
                    except Exception as e:
                        print(f"Error processing message: {e}")
                        await receiver.abandon_message(message)

    async def invoke_webhook(self, book_name: str, review_content: str):
        async with httpx.AsyncClient() as client:
            try:
                payload = {"book_title": book_name, "message": f"New review added: {review_content}"}
                response = await client.post(self.webhook_url, json=payload)
                if response.status_code == 200:
                    print("Webhook invoked successfully.")
                else:
                    print(f"Failed to invoke webhook: {response.status_code}, {response.text}")
            except Exception as e:
                print(f"Error invoking webhook: {e}")
                raise
