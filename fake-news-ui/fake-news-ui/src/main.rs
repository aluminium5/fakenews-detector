#[macro_use] extern crate rocket;

use rocket::form::Form;
use rocket::response::content::RawHtml;
use rocket::serde::{Deserialize, Serialize};
use reqwest::Client;

#[derive(FromForm)]
struct InputForm {
    text: String,
}

#[derive(Deserialize)]
struct Prediction {
    prediction: String,
}

#[get("/")]
fn index() -> RawHtml<&'static str> {
    RawHtml(r#"
        <form action="/predict" method="post">
            <textarea name="text" rows="5" cols="50" placeholder="Enter news text..."></textarea><br>
            <input type="submit" value="Check">
        </form>
    "#)
}

#[post("/predict", data = "<input>")]
async fn predict(input: Form<InputForm>) -> RawHtml<String> {
    let client = Client::new();
    let res = client.post("http://127.0.0.1:5000/predict")
        .json(&input.into_inner())
        .send()
        .await;

    match res {
        Ok(response) => {
            match response.json::<Prediction>().await {
                Ok(pred) => RawHtml(format!("<h2>Prediction: {}</h2>", pred.prediction)),
                Err(_) => RawHtml("<h2>Error parsing response</h2>".to_string()),
            }
        }
        Err(_) => RawHtml("<h2>Failed to connect to backend</h2>".to_string()),
    }
}

#[launch]
fn rocket() -> rocket::Rocket<rocket::Build> {
    rocket::build().mount("/", routes![index, predict])
}