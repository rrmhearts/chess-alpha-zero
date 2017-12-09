import sys

from chess_zero.agent.model_chess import ChessModel
from chess_zero.config import PlayWithHumanConfig
from chess_zero.lib.model_helper import load_best_model_weight
from chess_zero.uci.engine import Engine


def start(config):
    PlayWithHumanConfig().update_play_config(config.play)

    model = ChessModel(config)
    if not load_best_model_weight(model):
        raise RuntimeError("Best model not found!")
        sys.exit(-1)

    engine = Engine(config=config, model=model)

    while engine.running:
        uci_cmd = input().split()
        print("DEBUG: uci_cmd=" + str(uci_cmd), file=sys.stderr)
        if uci_cmd[0] in engine.uci_cmds:
            engine.args = uci_cmd[1:]
            engine.uci_cmds[uci_cmd[0]](engine)
        else:
            print("Unknown command: " + uci_cmd[0])
