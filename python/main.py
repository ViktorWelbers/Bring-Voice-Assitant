import grpc
from concurrent import futures

from llm import (
    setup_and_load_models,
    transcribe_audio,
    generate_new_shopping_list_item,
)
from protos import shopping_assistant_pb2_grpc
from protos import shopping_assistant_pb2

language_model, tokenizer, whisper_pipe = setup_and_load_models()


class ShoppingAssistantServicer(shopping_assistant_pb2_grpc.ShoppingAssistantServicer):
    def PostFileName(self, request, context):
        file_name = request.file_name
        print(f"Received file name {file_name}")
        transcribed_content = transcribe_audio(whisper_pipe, f"../{file_name}")
        new_shopping_list_item = generate_new_shopping_list_item(
            language_model, tokenizer, transcribed_content
        )
        return shopping_assistant_pb2.ShoppingListItemResponse(item=new_shopping_list_item.strip())


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    shopping_assistant_pb2_grpc.add_ShoppingAssistantServicer_to_server(
        ShoppingAssistantServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
