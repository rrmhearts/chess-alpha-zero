from chess_zero.agent.player_chess import ChessPlayer
from chess_zero.env.chess_env import ChessEnv

import chess


class Engine:
    def __init__(self, config, model):
        self.args = []  # Set by user
        self._env = ChessEnv()
        self._ai = ChessPlayer(config=config, model=model)
        self.running = True

    def uci(self):
        """
        Boot engine.
        """
        print("id name Alpha Zero")
        # TODO print author, options
        print("uciok")

    def debug(self):
        """
        Enable/disable debug mode.
        """
        # TODO

    def isready(self):
        """
        Engine ping.
        """
        print("readyok")

    def ucinewgame(self):
        """
        Start new game.
        """
        self._env.reset()

    def position(self):
        """
        Set position.
        """
        if self.args[0] == "startpos":
            self._env.reset()
            self.args = self.args[1:]
            if len(self.args) > 0 and self.args[0] == "moves":
                self.args = self.args[1:]
        else:
            # Set FEN
            self._env.update(self.args[0:6])
            self.args = self.args[1:]
        for i in range(0, len(self.args)):
            self._env.step(self.args[i])

    def go(self):
        """
        Start searching for moves.
        """
        # TODO process commands influencing search
        action = self._ai.action(self._env.observation)
        if action is None:
            # TODO Resign
            action = ""
        print("bestmove " + action)

    def stop(self):
        """
        Stop search for moves.
        """

    def quit(self):
        """
        Quit engine.
        """
        self.running = False

    uci_cmds = {
        "uci": uci,
        "debug": debug,
        "isready": isready,
        "ucinewgame": ucinewgame,
        "position": position,
        "go": go,
        "stop": stop,
        "quit": quit,
    }
