use std::process::Command;
use std::time::Duration;
mod http_client;
mod wav_recorder;

fn main() -> Result<(), anyhow::Error> {
    let file_name = "output.wav";
    let wav_path =
        wav_recorder::record_wav_from_microphone(Duration::from_secs(7), Some(file_name));
    println!("Wav file saved to: {:?}", wav_path);
    let result = http_client::get_file(file_name);
    let item = result.unwrap();
    println!("{:?}", item);
    let output = Command::new("bring")
        .arg("add")
        .arg(item)
        .output()
        .expect("failed to execute process");

    println!("status: {}", output.status);
    println!("stdout: {}", String::from_utf8_lossy(&output.stdout));
    println!("stderr: {}", String::from_utf8_lossy(&output.stderr));

    assert!(output.status.success());
    Ok(())
}
