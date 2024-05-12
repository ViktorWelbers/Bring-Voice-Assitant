use std::time::Duration;

mod wav_recorder;
fn main() -> Result<(), anyhow::Error> {
   let wav_path = wav_recorder::record_wav_from_microphone(Duration::from_secs(5), Some("output.wav"));
    println!("Wav file saved to: {:?}", wav_path);
    Ok(())
}
