// build.rs
fn main() {
    protoc_rust_grpc::Codegen::new()
        .out_dir("src/protos")
        .inputs(&["protos/shopping_assistant.proto"])
        .include("protos")
        .rust_protobuf(true) // also generate protobuf messages, not just services
        .run()
        .expect("protoc-rust-grpc");
}
