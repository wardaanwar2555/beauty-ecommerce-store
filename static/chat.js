fetch("/chat", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({ message: "What are your store hours?" })
})
.then(res => res.json())
.then(data => {
    console.log("Bot:", data.reply);
});
