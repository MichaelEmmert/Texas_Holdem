import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import base64
import TH

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

########################################################
########################################################
########################################################
################# Functions Used #######################
 

#these two functions calculate the probability of hitting each hand
def hand_ranked(hand):
    Texas_Holdem = TH.Table(hand,table,n_players)
    dealt = Texas_Holdem.deal()
    Holdem = TH.Hit_Hand(hand,dealt)
    return {
        'straight_flush' : Holdem.straight_flush(), #straight flush
        'four_of_kind' : Holdem.four_of_kind(),     #four of a kind
        'full_house' : Holdem.full_house(),         #full house
        'flush' : Holdem.flush(),                   #flush
        'straight' : Holdem.straight(),             #straight
        'three_of_kind' : Holdem.three_of_kind(),   #three of a kind
        'two_pair' : Holdem.two_pair(),             #two pair
        'pair' : Holdem.pair()                      #pair
        }


def probabilities(hand, n = 1000):    
    straight_flush = 0
    four_of_kind = 0
    full_house = 0
    flush = 0
    straight = 0
    three_of_kind = 0
    two_pair = 0
    pair = 0
    for i in range(n):        
        sim_hand = hand_ranked(hand)
        
        straight_flush += sim_hand['straight_flush'] #straight flush
        four_of_kind += sim_hand['four_of_kind'] #four of a kind
        full_house += sim_hand['full_house'] #full house
        flush += sim_hand['flush'] #flush
        straight += sim_hand['straight'] #straight
        three_of_kind += sim_hand['three_of_kind'] #three of a kind
        two_pair += sim_hand['two_pair'] #two pair
        pair += sim_hand['pair'] #pair
    return {'Straight Flush': (straight_flush/n)*100,
            'Four of a Kind': (four_of_kind/n)*100,
            'Full House': (full_house/n)*100,
            'Flush': (flush/n)*100,
            'Straight': (straight/n)*100,
            'Three of a Kind': (three_of_kind/n)*100,
            'Two Pair': (two_pair/n)*100,
            'Pair': (pair/n)*100}



#these functions determine the winning hand

#this function returns a "Top Hand" for the given input
def top_hand(hand):
    Texas_Holdem = TH.Table(hand,table,n_players)
    dealt = Texas_Holdem.deal()
    Holdem_hand = TH.Best_Hand(hand,dealt,print_hand = False)
    hands_form =  {
        'straight_flush' : Holdem_hand.straight_flush(), #straight flush
        'four_of_kind' : Holdem_hand.four_of_kind(),     #four of a kind
        'full_house' : Holdem_hand.full_house(),         #full house
        'flush' : Holdem_hand.flush(),                   #flush
        'straight' : Holdem_hand.straight(),             #straight
        'three_of_kind' : Holdem_hand.three_of_kind(),   #three of a kind
        'two_pair' : Holdem_hand.two_pair(),             #two pair
        'pair' : Holdem_hand.pair(),                     #pair
        'high_card': Holdem_hand.high_card()             #high card
    }
    i = 10
    for key, value in hands_form.items():
        i -= 1
        if value != None:
            return [(i,key), value]

#this function compares two hands to see who won

#PROBLEM RIGHT NOW IS IT IS CALLING top_hand() twice so the hand resets
def winner(hand,comparison_hand,print_details = False):
    p1 = top_hand(hand)
    p2 = top_hand(comparison_hand)
    if print_details == True:
        print('Cards on Table:\n', dealt[1], '\n\n')
        print('player 1 hand:', hand)
        print('Player 1:',p1)
        print('player 2 hand:', comparison_hand)
        print('Player 2:',p2)
        print('\n')

    if p1[0][0] > p2[0][0]:
        return True
    elif p1[0][0] == p2[0][0]:
        #compare each card starting at the most important
        for i in range(1,5):
            if p1[1][-i] > p2[1][-i]:
                return True
            elif p1[1][-i] < p2[1][-i]:
                return False   
        #if all cards are equal its a tie and we are calling ties wins because no money is lost in a tie
        return True 
    elif p1[0][0] < p2[0][0]:
        return False
    
#this calls winner as many times as necessary to see who won each hand            
def all_players(hand,other_players_hands):
    beat = []
    for player_hand in other_players_hands:
        beat.append(winner(hand,player_hand))
    return all(beat)
    
#this calculates the probability of winning
def winner_probabilty(hand, n = 1000):
    wins = 0
    for i in range(n):
        wins += all_players(hand,dealt[0])
    return (wins/n)*100
    

#these functions create a hand
def texas_holdem_selector(n_cards_on_table = 3, number_of_players = 5, kind = 'randomized'):
    global Game
    global Cards
    global p1
    global table
    global Texas_Holdem
    global dealt
    global Holdem
    global n_players
    global Holdem_hand
    n_players = number_of_players
    if kind == 'randomized':
        Game = TH.Hand()
        Cards = Game.player_1()
        p1 = Cards
        table = Game.table(cards_on_table = n_cards_on_table)
    elif kind == 'select_hand':
        Game = TH.Hand()
        Cards = Game.hand_selection()
        p1 = Cards
        table = Game.table_selection(cards_on_table = n_cards_on_table)        
    Texas_Holdem = TH.Table(Cards,table,n_players)
    dealt = Texas_Holdem.deal()

def texas_holdem_selector_list(number_of_players = 5,list_input_hand = [],list_input_table = [], display = False):
    global Game
    global Cards
    global p1
    global table
    global Texas_Holdem
    global dealt
    global Holdem
    global n_players
    cards_on_table = len(list_input_table)
    n_players = number_of_players
    Game = TH.Hand()
    Cards = Game.hand_selection_list(list_input_hand)
    p1 = Cards
    table = Game.table_selection_list(cards_on_table = list_input_table)        
    Texas_Holdem = TH.Table(Cards,table,n_players)
    dealt = Texas_Holdem.deal()

#this function allows for iteration over a list input
def list_input_iterator(full_hand,num_simulations = 100000,num_players = 3,display = False,batch = 0.01):
    mean = []
    sd = []
    number_of_hands = len(full_hand)
    x = 0
    for i in range(number_of_hands):
        x += 1
        texas_holdem_selector_list(number_of_players = num_players,list_input_hand = full_hand[i][0],
                                   list_input_table = full_hand[i][1], display = display)
        win_list = []
        for j in range(int(num_simulations*batch)):
            win = winner_probabilty(Cards, n = int(num_simulations/(num_simulations*batch)))
            win_list.append(win)
        y_upper = np.mean(win_list) + np.std(win_list)
        y_lower = np.mean(win_list) - np.std(win_list)
        mean.append(np.mean(win_list))
        sd.append([y_lower,y_upper])
        print(f'{x} of {number_of_hands} complete')
    return [mean, sd]

########################################################
########################################################
########################################################
########################################################


app = dash.Dash()

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
)

simulated_hands = 100
texas_holdem_selector(n_cards_on_table = 3, number_of_players = 5, kind = 'randomized') #randomized or select_hand
prob_of_hitting = probabilities(hand = Cards, n = simulated_hands)
probability_of_winning = winner_probabilty(Cards, n = simulated_hands)


Y, X = zip(*prob_of_hitting.items())

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("poker_chips.png"),
                            id="aces-image",
                            style={
                                "height": "100px",
                                "width": "auto",
                                "margin-bottom": "5px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Texas Holdem Simulator",
                                    style={"margin-bottom": "5px"},
                                )
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("About Me", id="about-me-button"),
                            href="https://medium.com/@michaelemmert1234",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "5px"},
        ),
        html.Div(
            [
                html.Div(
                    # dcc.Tabs([
                    #     dcc.Tab(label = "Randomized Opion",children = [
                    #         html.Div([
                    [
                        dcc.RadioItems(
                            id = 'rand-selected',
                            options=[
                                {'label': 'Selected Cards', 'value': 'selected_cards'},
                                {'label': 'Randomized Cards', 'value': 'randomized_cards'},
                            ],
                            value= 'selected_cards',
                            labelStyle={'display': 'inline-block'}
                        ),
                        html.H6(
                            "Number of players sitting at the Table:",
                            className="control_label",
                        ),
                        dcc.Slider(
                            id='num-players',
                            min=2, 
                            max=10, 
                            step=1, 
                            value=3,
                                marks={
                                    2: '2',
                                    3: '3',
                                    4: '4',
                                    5: '5',
                                    6: '6',
                                    7: '7',
                                    8: '8',
                                    9: '9',
                                    10: '10',
                                },
                            className="dcc_control"
                        ),
                        html.H6(
                            "Number of Cards on the Table:",
                            className="control_label",
                        ),
                        dcc.RadioItems(
                            id = 'number-cards-displayed',
                            options=[
                                {'label': 'Zero', 'value': 0},
                                {'label': 'Three', 'value': 3},
                                {'label': 'Four', 'value': 4}
                            ],
                            value= 3
                        ),
                        html.H6("Number of Hands Simulated:", className="control_label"),
                        dcc.Dropdown(
                            id='num-sims',
                            options=[
                                {'label': '1,000', 'value': 1000},
                                {'label': '10,000', 'value': 10000},
                                {'label': '100,000', 'value': 100000},
                                {'label': '1,000,000', 'value': 100000}
                            ],
                            value=1000,
                            className="dcc_control",
                        ),
                        # dcc.Dropdown(
                        #     id='card2-selection-input',
                        #     options=[
                        #         {'label': '2♥️', 'value': "(2, 'H')"},
                        #         {'label': '2♦️', 'value': "(2, 'D')"},
                        #         {'label': '2♠️', 'value': "(2, 'S')"},
                        #         {'label': '2♣️', 'value': "(2, 'C')"}
                        #     ],
                        #     value="(2, 'D')"
                        # ),
                        html.Button(
                            'Update',
                            id = 'Randomize-Button',
                            className = 'dcc_control'
                        ),
                    ],
                   className="pretty_container four columns",
                   id="cross-filter-options"
                ),

                html.Div(
                    [
                    html.Div(
                        [
                        html.Div(
                            [
                            html.H6("Your Hand:"),
                            dcc.Dropdown(
                                id='card1-selection-input',
                                options=[
                                    {'label': '2♥️', 'value': "(2, 'H')"},
                                    {'label': '2♦️', 'value': "(2, 'D')"},
                                    {'label': '2♠️', 'value': "(2, 'S')"},
                                    {'label': '2♣️', 'value': "(2, 'C')"}
                                ],
                                value="(2, 'C')"
                            ),
                            dcc.Dropdown(
                                id='card2-selection-input',
                                options=[
                                    {'label': '2♥️', 'value': "(2, 'H')"},
                                    {'label': '2♦️', 'value': "(2, 'D')"},
                                    {'label': '2♠️', 'value': "(2, 'S')"},
                                    {'label': '2♣️', 'value': "(2, 'C')"}
                                ],
                                value="(2, 'C')"
                            ),
                            html.Img(id='Card1-image', width = 100, height = 170),
                            html.Img(id='Card2-image', width = 100, height = 170),
                            ],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                        ]),
                        html.Div(
                            [
                            html.H6("Cards on the Table:"),
                            dcc.Dropdown(
                                id = 'cards-on-table',
                                options=[
                                    {'label': '3♥️', 'value': "(3, 'H')"},
                                    {'label': '3♦️', 'value': "(3, 'D')"},
                                    {'label': '3♠️', 'value': "(3, 'S')"},
                                    {'label': '3♣️', 'value': "(3, 'C')"},
                                    {'label': '4♥️', 'value': "(4, 'H')"},
                                    {'label': '4♦️', 'value': "(4, 'D')"},
                                    {'label': '4♠️', 'value': "(4, 'S')"},
                                    {'label': '4♣️', 'value': "(4, 'C')"}
                                ],
                                value=["(4, 'D')", "(4, 'C')","(3, 'S')"],
                                multi=True
                            ),
                            html.Img(id='Card3-image', width = 100, height = 170),
                            html.Img(id='Card4-image', width = 100, height = 170),
                            html.Img(id='Card5-image', width = 100, height = 170),
                            html.Img(id='Card6-image', width = 100, height = 170)
                            ],
                            className="pretty_container"
                        )
                    ],
                    className="five columns",
                ),

                html.Div(
                    [
                    dcc.Graph(id='Randomize-Button-win')
                    ],
                    className="pretty_container three columns",
                        )
                    ],
                    className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [
                    dcc.Graph(id='Randomize-Button-hand')
                    ],
                    className="pretty_container twelve columns",
                )
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


# #Call backs
@app.callback(
    [
        dash.dependencies.Output('Randomize-Button-hand', 'figure'), 
        dash.dependencies.Output('Randomize-Button-win', 'figure'),
        dash.dependencies.Output('Card1-image', 'src'),
        dash.dependencies.Output('Card2-image', 'src'),
        dash.dependencies.Output('Card3-image', 'src'),
        dash.dependencies.Output('Card4-image', 'src'),
        dash.dependencies.Output('Card5-image', 'src'),
        dash.dependencies.Output('Card6-image', 'src')
    ],
    [dash.dependencies.Input('Randomize-Button', 'n_clicks')],
    [
        dash.dependencies.State('rand-selected', 'value'),
        dash.dependencies.State('num-players', 'value'),
        dash.dependencies.State('number-cards-displayed', 'value'),
        dash.dependencies.State('num-sims', 'value'),
        dash.dependencies.State('cards-on-table', 'value'),
        dash.dependencies.State('card1-selection-input', 'value'),
        dash.dependencies.State('card2-selection-input', 'value')
    ]
    )

def randomized(n_clicks,rand_selected = 'selected_cards', n_players_input = 2,cards_displayed = 3,num_sims = 1000,
    cards_on_table = ["(4, 'D')", "(4, 'C')","(3, 'S')"], card1_selection_input = "(2, 'C')",card2_selection_input = "(2, 'H')"):
    simulated_hands = num_sims
    if rand_selected == 'selected_cards':
        ##TABLE##

        hand_selected = [eval(card1_selection_input),eval(card2_selection_input)]
        table_cards = []
        for card in cards_on_table:
            table_cards.append(eval(card))

        texas_holdem_selector_list(number_of_players = n_players_input,list_input_hand = hand_selected,list_input_table = table_cards)


    elif rand_selected == 'randomized_cards':
        texas_holdem_selector(n_cards_on_table = cards_displayed, number_of_players = n_players_input, kind = 'randomized')
    ################
    player_card1 = f'assets/cards/{str(Cards[0][0]) + Cards[0][1]}.PNG'
    player_card2 = f'assets/cards/{str(Cards[1][0]) + Cards[1][1]}.PNG'
    if cards_displayed == 0:
        table1 = 'assets/cards/gray_back.PNG'
        table2 = 'assets/cards/gray_back.PNG'
        table3 = 'assets/cards/gray_back.PNG'
        table4 = 'assets/cards/gray_back.PNG'

    elif cards_displayed == 3:
        table1 = f'assets/cards/{str(table[0][0][0]) + table[0][0][1]}.PNG'
        table2 = f'assets/cards/{str(table[0][1][0]) + table[0][1][1]}.PNG'
        table3 = f'assets/cards/{str(table[0][2][0]) + table[0][2][1]}.PNG'
        table4 = 'assets/cards/gray_back.PNG'
    elif cards_displayed == 4:
        table1 = f'assets/cards/{str(table[0][0][0]) + table[0][0][1]}.PNG'
        table2 = f'assets/cards/{str(table[0][1][0]) + table[0][1][1]}.PNG'
        table3 = f'assets/cards/{str(table[0][2][0]) + table[0][2][1]}.PNG'
        table4 = f'assets/cards/{str(table[0][3][0]) + table[0][3][1]}.PNG'


    card1_base64 = 'data:image/png;base64,' + base64.b64encode(open(player_card1, 'rb').read()).decode('ascii')
    card2_base64 = 'data:image/png;base64,' + base64.b64encode(open(player_card2, 'rb').read()).decode('ascii')
    card3_base64 = 'data:image/png;base64,' + base64.b64encode(open(table1, 'rb').read()).decode('ascii')
    card4_base64 = 'data:image/png;base64,' + base64.b64encode(open(table2, 'rb').read()).decode('ascii')
    card5_base64 = 'data:image/png;base64,' + base64.b64encode(open(table3, 'rb').read()).decode('ascii')
    card6_base64 = 'data:image/png;base64,' + base64.b64encode(open(table4, 'rb').read()).decode('ascii')
    ################
    prob_of_hitting = probabilities(hand = Cards, n = simulated_hands)
    probability_of_winning = winner_probabilty(Cards, n = simulated_hands)

    Y, X = zip(*prob_of_hitting.items())
    hand_hit_graph = {
            'data': [{'x':X,'y':Y, 'type':'bar', 'name':'Example','orientation':'h'}],
        'layout':{
            'title':'Probability of Hitting Each Hand',
            "showlegend": False,
            "marker": {"bar": {"color": "white", "width": 1}},
            'plot_bgcolor': "#F9F9F9",
            'paper_bgcolor': "#F9F9F9",
            'orientation':'h',
                        "xaxis": {
                "side": "bottom",
                "type": "linear",
                "range": [0,100]
                    },
            'margin':{
                'l':120,
                'r':50,
                'b':50,
                't':50,
                'pad':4
            }
            }
        }
    winner_graph =  {
    'data': [{'x':['Probability of Winning'],'y':[probability_of_winning], 'type':'bar', 'name':'Probability of winning'}],
    'layout':{'title':'Probability of Winning',
            "showlegend": False,
            "marker": {"bar": {"color": "white", "width": 1}},
           'plot_bgcolor': "#F9F9F9",
           'paper_bgcolor': "#F9F9F9",
            "yaxis": {
                "side": "bottom",
                "type": "linear",
                "range": [0,100]
                    },
            'margin':{
                'l':50,
                'r':50,
                'b':50,
                't':50,
                'pad':0
            }
            }
        }
    return [hand_hit_graph, winner_graph, card1_base64, card2_base64, card3_base64, card4_base64, card5_base64,card6_base64]


if __name__ == '__main__':
	app.run_server(debug = True)