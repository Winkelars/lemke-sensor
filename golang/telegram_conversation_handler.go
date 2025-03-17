package main

import (
	"fmt"
	"log"
	"os"
	"sync"

	"github.com/PaulSonOfLars/gotgbot/v2"
	"github.com/PaulSonOfLars/gotgbot/v2/ext"
	"github.com/PaulSonOfLars/gotgbot/v2/ext/handlers"
)

// Thread-sichere Liste der abonnierten Nutzer
var subscribedUsers = struct {
	sync.RWMutex
	ids map[int64]struct{}
}{ids: make(map[int64]struct{})}

// Sendet eine Nachricht an alle abonnierten Nutzer
func SendMessageToSubscribers(bot *gotgbot.Bot, message string) {
	subscribedUsers.RLock()
	defer subscribedUsers.RUnlock()

	for userID := range subscribedUsers.ids {
		_, err := bot.SendMessage(userID, message, nil)
		if err != nil {
			log.Printf("Fehler beim Senden an %d: %s", userID, err)
		}
	}
}

// Telegram-Bot starten und `bot`-Objekt zurückgeben
func ConversationHandler() *gotgbot.Bot {
	token := os.Getenv("TOKEN")
	if token == "" {
		panic("TOKEN environment variable is empty")
	}

	bot, err := gotgbot.NewBot(token, nil)
	if err != nil {
		panic("failed to create new bot: " + err.Error())
	}

	dispatcher := ext.NewDispatcher(nil)
	updater := ext.NewUpdater(dispatcher, nil)

	// Start- und Subscribe-Handler registrieren
	dispatcher.AddHandler(handlers.NewCommand("start", start))
	dispatcher.AddHandler(handlers.NewCommand("subscribe", subscribe))
	dispatcher.AddHandler(handlers.NewCommand("unsubscribe", unsubscribe))

	// Polling starten
	err = updater.StartPolling(bot, &ext.PollingOpts{DropPendingUpdates: true})
	if err != nil {
		panic("failed to start polling: " + err.Error())
	}

	log.Printf("%s has been started...\n", bot.User.Username)
	go updater.Idle() // Damit der Bot weiterläuft

	return bot // Bot-Objekt zurückgeben
}

// Start-Nachricht
func start(bot *gotgbot.Bot, ctx *ext.Context) error {
	_, err := ctx.EffectiveMessage.Reply(bot, "Willkommen! Nutze /subscribe, um Benachrichtigungen zu erhalten.", nil)
	return err
}

// Nutzer zum Abo hinzufügen
func subscribe(bot *gotgbot.Bot, ctx *ext.Context) error {
	userID := ctx.EffectiveMessage.Chat.Id

	subscribedUsers.Lock()
	subscribedUsers.ids[userID] = struct{}{}
	subscribedUsers.Unlock()

	_, err := ctx.EffectiveMessage.Reply(bot, "Du hast dich erfolgreich für Benachrichtigungen angemeldet!\n\nNutze /unsubscribe falls du keine Benachrichtigungen mehr erhalten möchtest.", nil)
	fmt.Printf("Nutzer %d hat sich angemeldet\n", userID)
	return err
}

func unsubscribe(bot *gotgbot.Bot, ctx *ext.Context) error {
	userID := ctx.EffectiveMessage.Chat.Id

	subscribedUsers.Lock()
	delete(subscribedUsers.ids, userID)
	subscribedUsers.Unlock()

	_, err := ctx.EffectiveMessage.Reply(bot, "Du hast dich erfolgreich von Benachrichtigungen abgemeldet!\n\nNutze /subscribe falls du wieder Benachrichtigungen erhalten möchtest.", nil)
	fmt.Printf("Nutzer %d hat sich abgemeldet\n", userID)
	return err
}
