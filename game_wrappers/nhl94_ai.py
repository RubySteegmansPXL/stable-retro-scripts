"""
NHL AI
Very simple hard coded AI for testing purposes
"""

import math
import random
from game_wrappers.nhl94_const import GameConsts
from game_wrappers.nhl94_gamestate import NHL94GameState

AI_STATE_IDLE = 0
AI_STATE_ISHOOTING = 1

from models import init_model


class NHL94AISystem():
    def __init__(self, args, env, logger):
        self.test = 0
        self.args = args
        self.use_model = True
        self.p1_model = None
        self.state = AI_STATE_IDLE
        if args.load_p1_model is '':
            self.use_model = False
        else:
            self.p1_model = init_model(None, args.load_p1_model, args.alg, args, env, logger)

        self.get_puck_model = None
        self.score_goal_model = None

        self.logger = logger
        self.env = env

        self.target_xy = [0,0]

        self.scoregoal_state = None

        self.game_state = NHL94GameState()

    def SetModels(self, get_puck_model_path, score_goal_model_path):
        if get_puck_model_path != '' and score_goal_model_path != '':
            print(get_puck_model_path)
            print(score_goal_model_path)
            self.get_puck_model = init_model(None, get_puck_model_path, self.args.alg, self.args, self.env, self.logger)
            self.score_goal_model = init_model(None, score_goal_model_path, self.args.alg, self.args, self.env, self.logger)

    def GotoTarget(self, p1_actions, target_vec):
        if target_vec[0] > 0:
            p1_actions[GameConsts.INPUT_LEFT] = 1
        else:
            p1_actions[GameConsts.INPUT_RIGHT] = 1

        if target_vec[1] > 0:
            p1_actions[GameConsts.INPUT_DOWN] = 1
        else:
            p1_actions[GameConsts.INPUT_UP] = 1

    def DistToPos(self, vec1, vec2):
        tmp = (vec1[0] - vec2[0])**2 + (vec1[1] - vec2[1])**2
    
        return math.sqrt(tmp)

    def Think_TwoModels(self, info, state, deterministic):

        p1_actions = [0] * GameConsts.INPUT_MAX

        p1_x = info.get('p1_x')
        p1_y = info.get('p1_y')
        g1_x = info.get('g1_x')
        g1_y = info.get('g1_y')
        puck_x = info.get('puck_x')
        puck_y = info.get('puck_y')
        fullstar_x = info.get('fullstar_x')
        fullstar_y = info.get('fullstar_y')


        player_haspuck = False
        goalie_haspuck = False

        if(p1_x == fullstar_x and p1_y == fullstar_y):
            player_haspuck = True
        elif(g1_x == fullstar_x and g1_y == fullstar_y):
            goalie_haspuck = True


        if player_haspuck:
            p1_actions = self.score_goal_model.predict(state, deterministic=deterministic)

        elif goalie_haspuck:
            p1_actions[GameConsts.INPUT_B] = 1
            return [[p1_actions]]
            print('GOALIE PASS')
        else:
            p1_actions = self.get_puck_model.predict(state, deterministic=deterministic)

        return p1_actions

    def SelectRandomTarget(self):
        x = (random.random() - 0.5) * 240
        y = (random.random() - 0.5) * 460

        return [x,y]

    def Think_GotoRandomTarget(self, state):
        p1_actions = [0] * GameConsts.INPUT_MAX

        pp_vec = [state.p1_x - state.puck_x, state.p1_y - state.puck_y]
        tmp = (state.p1_x - state.puck_x)**2 + (state.p1_y - state.puck_y)**2
        pp_dist = math.sqrt(tmp)

        #if(state.goalie_haspuck): print('GOALIE HAS PUCK')

        if state.player_haspuck:
            dist = self.DistToPos([state.p1_x, state.p1_y], self.target_xy)

            if dist < 20.0:
                self.target_xy = self.SelectRandomTarget()
                #print(self.target_xy)
                r = random.random()
                #print(r)
                if r < 0.2:
                    p1_actions[GameConsts.INPUT_B] = 1

            # TODO check if target is near opposing player
            self.GotoTarget(p1_actions, [state.p1_x - self.target_xy[0], state.p1_y - self.target_xy[1]])

        elif state.goalie_haspuck:
            p1_actions[GameConsts.INPUT_B] = 1
            #print('GOALIE PASS')
        else:
            self.GotoTarget(p1_actions, pp_vec)
            #print('FIND PUCK')

        return p1_actions
    
    def Think_ScoreGoal01(self, state):
        p1_actions = [0] * GameConsts.INPUT_MAX

        dist = self.DistToPos([state.p1_x, state.p1_y], [GameConsts.SHOOT_POS_X, GameConsts.SHOOT_POS_Y])

        if dist < 60:
            p1_actions[GameConsts.INPUT_C] = 1
        else:
            self.GotoTarget(p1_actions, [state.p1_x - GameConsts.SHOOT_POS_X, state.p1_y - GameConsts.SHOOT_POS_Y])

        return p1_actions

        
    def Think_ScoreGoal02(self, state):
        p1_actions = [0] * GameConsts.INPUT_MAX

        if self.scoregoal_state == None:
            #choose target on left side
            dist = self.DistToPos([state.p1_x, state.p1_y], [90, 200])

            if dist < 50:
                self.scoregoal_state = "On left side"
            else:
                self.GotoTarget(p1_actions, [state.p1_x - (90), state.p1_y - 200])
                    #print('GOTO SHOOT POSITION')
        
        if self.scoregoal_state == "On left side":
            dist = self.DistToPos([state.p1_x, state.p1_y], [-80, 200])

            if dist < 50:
                self.scoregoal_state = "On right side"
            else:
                self.GotoTarget(p1_actions, [state.p1_x - (-80), state.p1_y - 200])

        if self.scoregoal_state == "On right side":
            p1_actions[GameConsts.INPUT_C] = 1
            self.scoregoal_state = None

        return p1_actions



    def Think_testAI(self, state):
        p1_actions = [0] * GameConsts.INPUT_MAX

        pp_vec = [state.p1_x - state.puck_x, state.p1_y - state.puck_y]
        tmp = (state.p1_x - state.puck_x)**2 + (state.p1_y - state.puck_y)**2
        pp_dist = math.sqrt(tmp)

        #if(state.goalie_haspuck): print('GOALIE HAS PUCK')

        if state.player_haspuck:
            

            p1_actions = self.Think_ScoreGoal02(state)
           
        elif state.goalie_haspuck:
            self.scoregoal_state = None
            p1_actions[GameConsts.INPUT_B] = 1
            #print('GOALIE PASS')
        else:
            self.scoregoal_state = None
            self.GotoTarget(p1_actions, pp_vec)
            #print('FIND PUCK')

        return p1_actions

    def predict(self, state, info, deterministic):
        if info is None:
            p1_actions = [[0] * GameConsts.INPUT_MAX]
            return p1_actions
        
        self.game_state.BeginFrame(info[0])
        
        if self.use_model:
            p1_actions = self.p1_model.predict(state, deterministic=deterministic)[0]
        elif self.get_puck_model and self.score_goal_model:
            p1_actions = self.Think_TwoModels(info[0], state, deterministic)[0]
        else:          
            p1_actions = [self.Think_testAI(self.game_state)]

        self.game_state.EndFrame()

        return p1_actions

    