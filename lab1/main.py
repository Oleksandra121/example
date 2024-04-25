from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label  # Додаємо імпорт Label
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    winner_label = ObjectProperty(None)
    def start_game(self):
        Clock.unschedule(self.update)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def pause_game(self):
        Clock.unschedule(self.update)

    def reset_game(self):
        self.pause_game()
        self.player1.score = 0
        self.player2.score = 0
        self.serve_ball()

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
            self.check_winner()  # Додайте цей рядок
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))
            self.check_winner()  # І цей рядок

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

    def check_winner(self):
        if self.player1.score >= 10:
            self.winner_label.text = "Player 1 wins"
            self.display_winner()
        elif self.player2.score >= 10:
            self.winner_label.text = "Player 2 wins"
            self.display_winner()

    def display_winner(self):
        self.winner_label.center_x = self.width / 2
        self.winner_label.center_y = self.height / 3
        self.winner_label.text = self.winner_label.text.upper()
        if not self.winner_label.parent:
            self.add_widget(self.winner_label)
        Clock.unschedule(self.update)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel
        if self.winner_label:
            self.winner_label.text = ''
            if self.winner_label.parent:
                self.remove_widget(self.winner_label)

class PongApp(App):
    def build(self):
        game = PongGame()
        winner_label = Label()  # Створюємо Label для winner_label
        game.add_widget(winner_label)
        game.winner_label = winner_label
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    PongApp().run()
