use reqwest::Error;

pub fn get_file(file_name: &str) -> Result<String, Error> {
    let response = reqwest::blocking::get(format!(
        "http://localhost:8000/local?file_name={}",
        file_name
    ));
    let body = response?.text()?;
    Ok(body)
}
