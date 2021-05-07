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
       '<b>Please note that you have 8 minutes to read these instructions. <br>'
       'After that the game will start automatically.</b>'
       '</p>',

    2: '<p>'
       'In the game there are <b>two types</b> of players: the <b style="color: #5893f6">blue</b> and <b style="color: #d4c84d">yellow</b> one.'
       'You will be randomly attributed to one color in the beginning of the game.'
       'Your type will <b>remain</b> the same all along the game.<br>'
       'Note that different types have different multipliers (the latter is displayed on the character tshirt).'
       '<br><br><div align="center"><img src="/static/img/2_players.png"><br><br></div>'
       'In each round you will be randomly matched with another player. A round is divided into 3 steps.<br>'
       '1) You will be asked to either display or hide your multiplier, so that the other player will know your type or not.<br>'
       '2) You will be asked to contribute (a certain number of points) to a public pot.<br>'
       '3) Your contribution will be multiplied according to your type and the points put in the public pot will be equally distributed among the players. <br>'
       'Thereafter, you will continue to the next round.'
       '</p>',

    3: '<p>'
       'In the beginning of each round you will be presented with your character and its multiplier. '
       'You will be also asked whether or not you want to <b>disclose it</b>.<br> '
       'If you choose to disclose it, the <b>other player</b> will be <b>informed</b> of this information in the contribution step (he will see your character on his screen). '
       'Conversely, if you choose to hide it, the <b>other player</b> will see your character hiding his multiplier by means of a sign in the <b>contribution step</b>.<br>'
       '<br>Suppose you were attributed the <b style="color: #5893f6">blue</b> type and the other player the <b style="color: #d4c84d">yellow</b>,'
       'then there are 4 possible "disclosure" situations:<br><br>'
       '<b>1) You both disclose</b> <br><br>' + two_players(1.2, 0.8, 1.2, 0.8) +
       '<b>2) You both hide</b> <br><br>' + two_players(None, None, '...', '...') +
       '<b>3) You disclose and the other player hides</b> <br><br>' + two_players(1.2, None, 1.2, '...') +
       '<b>4) You hide and the other player discloses</b> <br><br>' + two_players(None, 0.8, '...', 0.8) +
       '<p>',

    4: '<p>'
       'In the second step of the round, you will see the outcome of the previous decision, that is one of the 4 disclosure situations.'
       'Also, in each round, you will be endowed with 10 points, and asked to contribute to the public pot. You will be able to do so '
       'using a slider, which value corresponds to the number of points you want to put in the public pot.'
       '</p>'
}

titles = {
    1: 'Welcome!',
    2: 'Short summary of the game',
    3: 'Disclosure',
    4: 'Contribution',
    5: 'Results',
}


