def two_players(m1, m2, t1, t2):
    s = f'''<div class="row">
    <div class="col">
    <div class="box" align="center">
    <img width="80%" src="/static/img/{m1}.gif">
    <div class="text-centered">{t1}</div>
    </div>
    </div>
    <div class="col">
    <div class="box" align="center">
    <img width="80%" style="-webkit-transform: scaleX(-1);transform: scaleX(-1);" src="/static/img/{m2}.gif">
    <div style="left: 6%" class="text-centered">{t2}</div>
    </div>
    </div>
    </div><br><br>'''
    return s


panels = {
    1: '<p>'
       'You are about to participate in an experiment on decision-making in economics. '
       'This study is based on your voluntary participation and your data will be treated confidentially and anonymously.'
       'This experiment is composed of three phases: <br>'
       '1) Instructions<br>'
       '2) A game<br>'
       '3) A short survey<br>'
       '<b>Please note that from now on you have 10 minutes to read these instructions. <br>'
       'After that the game will start automatically.</b>'
       '</p>',

    2: '<p>'
       'In the game there are <b>two types</b> of players: the <b style="color: #5893f6">blue</b> and <b style="color: #d4c84d">yellow</b> one.'
       'You will be randomly attributed to one color in the beginning of the game.'
       'Your type will <b>remain</b> the same all along the game.<br>'
       'Note that different types have different multipliers (the latter is displayed on the character t-shirt).'
       '<br><br><div align="center"><img src="/static/img/2_players.png"><br><br></div>'
       'In total there are <b>60 rounds</b>. In each round you will be randomly matched with another player. A round is divided into 3 steps:<br><br>'
       '1) You will be asked if you want to either display or hide your multiplier, so that the other player will know your type or not.<br><br>'
       '2) You will be asked to contribute (a certain number of points) to a public pot.<br><br>'
       '3) Your contribution will be multiplied according to your type and the points put in the public pot'
       ' will be equally distributed among the players. <br><br>'
       'Thereafter, you will continue to the next round.'
       '</p>',

    3: '<p>'
       'In the beginning of each round you will be presented with your character and your multiplier. '
       'You will be also asked whether or not you want to <b>disclose it</b>.<br> '
       'If you choose to disclose it, the <b>other player</b> will be <b>informed</b> of this information'
       ' in the contribution step (she/he will see your character on her/his screen). '
       'Conversely, if you choose to hide it, the <b>other player</b> will see your character hiding her/his multiplier'
       ' by means of a sign in the <b>contribution step</b>.<br>'
       '<br>Suppose you were attributed the <b style="color: #5893f6">blue</b> type and the other player the <b style="color: #d4c84d">yellow</b>'
       '. There are 4 possible "disclosure" situations:<br><br>'
       '<b>1) You both disclose</b> <br><br>' + two_players(1.2, 0.8, 1.2, 0.8) +
       '<b>2) You both hide</b> <br><br>' + two_players(None, None, '...', '...') +
       '<b>3) You disclose and the other player hides</b> <br><br>' + two_players(1.2, None, 1.2, '...') +
       '<b>4) You hide and the other player discloses</b> <br><br>' + two_players(None, 0.8, '...', 0.8) +
       '<br><br><b> Please note that you have 30 seconds to choose to disclose or hide your multiplier, if you take more time, you will be disconnected.<br>'
       '<p>',

    4: '<p>'
       'In the second step of the round, you will see the outcome of the previous decision, that is one of the <b>4 "disclosure" situations</b>.'
       '<br><br>Also, in each round, your private wallet  will be <b>endowed with 10 points</b>, and you will be asked to contribute to the public pot. You will be able to do so '
       'using a slider, which value corresponds to the number of points you want to put in the public pot. <br>'
       'To select a value on the slider you can either select with your mouse cursor, eitheir using your left and right arrow keys on your keyboard.'
       ' The maximum contribution is 10, while the minimum is 0.<br>'
       '<br><div align="center"><img src="/static/img/contribute.gif"><br></div>'
       '<br><b> Please note that you have 30 seconds to give your contribution, if you take more time, you will be disconnected.<br>'
       '</p>',
    5: '<p>'
       'In the third step of the round, you will see the <b>outcome</b> of the <b>contribution step</b>. '
       'Your type, as well as the type of the player with whom you have played will be revealed.<br>'#Also, both players type will be displayed, whether or not you or the other player chose to disclose in the previous steps.'
       '<br><br>Suppose you are a <b style="color: #d4c84d">yellow</b> player, your contribution to the public pot will be multiplied by <b style="color: #d4c84d">0.8</b>. '
       'Suppose you chose to contribute 10 points to the public pot, then your final contribution will be 8 because 10x<b style="color: #d4c84d">0.8</b> = 8.<br>'
       '<br>Suppose the other player is <b style="color: #5893f6">blue</b> and chose to contribute also 10 points to the public pot, '
       ' then his/her final contribution will be 12 because 10x <b style="color: #5893f6">1.2</b> = 12 <br>'
       '<br><br>The total contribution (the sum of both player contribution) is then distributed equally among the players such that:<br>'
       '<div align="center">IND. SHARE = 10 = ((10x<b style="color: #d4c84d">0.8</b>) + (10x<b style="color: #5893f6">1.2</b>))/2</div>'
        '<br>It means that both player individual share is 10 points for this hypothetical round. <br><br>'
       '<b>Please note that the payoff you will receive is your individual share added to the points left in your private wallet. In the fictional example above, there are no points letft '
       'in your private wallet because you contributed the maximum number of points.<b><br><br>'
       '<b>Please note that payoffs from all the 10 rounds are summed at the end of the experiment. This sum is used to compute your bonus compensation.</b><br><br>'
       'Regarding your bonus compensation, here is the conversion: <br>'
       ' 1 point = 0.5 pence <br>'
       ' 200 points = 1 pound <br>'
       'Note that you can win up to 5 pounds as a bonus compensation.'
       '</p>',
    6: '<p>'
       '<br><br><b> The game will start in time seconds.</b>'
        '<p>'

}

titles = {
    1: 'Welcome!',
    2: 'Short summary of the game',
    3: 'Disclosure',
    4: 'Contribution',
    5: 'Results',
    6: 'End of the instructions'
}
