package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/PaulSonOfLars/gotgbot/v2"
)

type LogMessage struct {
	Message string `json:"message"`
}

var bot *gotgbot.Bot

func logHandler(w http.ResponseWriter, r *http.Request) {
	var logMsg LogMessage
	err := json.NewDecoder(r.Body).Decode(&logMsg)
	if err != nil {
		http.Error(w, "Error decoding request body", http.StatusBadRequest)
		return
	}
	fmt.Println("Log-Nachricht erhalten.")

	if bot != nil {
		SendMessageToSubscribers(bot, logMsg.Message)
	}

	w.WriteHeader(http.StatusOK)
}

func Listen(b *gotgbot.Bot) {
	bot = b
	http.HandleFunc("/log", logHandler)
	fmt.Println("Golang-Server läuft auf Port 8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
