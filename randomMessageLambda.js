const messages = [
    { id: 1, message: "Hola, mundo!" },
    { id: 2, message: "Bienvenido a la arquitectura de microservicios." },
    { id: 3, message: "¡AWS Lambda es increíble!" },
    { id: 4, message: "Microservicios simplificados." },
    { id: 5, message: "¡Ten un gran día!" }
];

exports.handler = async (event) => {
    const randomIndex = Math.floor(Math.random() * messages.length);
    const randomMessage = messages[randomIndex];

    console.log("Random message selected:", randomMessage);

    return {
        statusCode: 200,
        body: JSON.stringify(randomMessage),
        headers: {
            "Content-Type": "application/json"
        }
    };
};