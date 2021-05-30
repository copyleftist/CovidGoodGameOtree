from settings import pounds_per_point
from step1.models import Constants
import numpy as np


def two_players(m1, m2, t1, t2):
    s = f'''<div class="row">
    <div class="col">
    <div class="box" align="center">
    <img width="80%" src="/static/img/{m1}.gif">
    <div style="font-size: 25px" class="text-centered">{t1}</div>
    </div>
    </div>
    <div class="col">
    <div class="box" align="center">
    <img width="80%" style="-webkit-transform: scaleX(-1);transform: scaleX(-1);" src="/static/img/{m2}.gif">
    <div style="left: 6%; font-size: 25px;" class="text-centered">{t2}</div>
    </div>
    </div>
    </div><br><br>'''
    return s

panels = {
    1: '<p>'
       'You are about to participate in an experiment on decision-making in economics. '
       'This study is based on your voluntary participation and your data will be treated confidentially and anonymously.'
       'This experiment is composed of four phases: <br>'
       '1) Instructions<br>'
       '2) A short training game.<br>'
       '3) A game<br>'
       '4) A short survey<br>'
       '<b>Please note that from now on you have 9 minutes to read these instructions. <br>'
       'After that the game will start automatically.</b>'
       '</p>',

    2: '<p>'
       'In the game there are <b>two types</b> of players: the <b style="color: #5893f6">blue</b> and <b style="color: #d4c84d">yellow</b> one.'
       'You will be randomly attributed to one color in the beginning of the game.'
       'Your type will <b>remain</b> the same all along the game.<br>'
       'Note that different types have different multipliers (the latter is displayed on the character t-shirt).'
       '<br><br>' + two_players(Constants.multiplier_good, Constants.multiplier_bad, Constants.multiplier_good, Constants.multiplier_bad) +
       f'In total there are <b>{Constants.num_rounds - 3} rounds</b> (+ 3 training rounds). '
       f'A round is divided into 3 steps:<br><br>'
       '1) You will be asked if you want to either disclose or hide your multiplier to the experimenter, who then decides to reveal it to your partner or not.<br><br>'
       '2) You will be asked to contribute (a certain number of points) to a public pot.<br><br>'
       '3) Your contribution will be multiplied according to your type and the points put in the public pot'
       ' will be equally distributed among the players. <br><br>'
       'Thereafter, you will continue to the next round.<br>',

    3: '<p>'
       'In the beginning of each round you will be presented with your character and your multiplier. '
       'You will be also asked whether or not you want to <b>disclose it</b>.<br> '
       'If you choose to disclose it, the <b>experimenter</b> will decide to reveal or hide this information to your <b>partner</b>'
       " in the contribution step (she/he will see (or not) your character on her/his screen) depending on the experimenter's decision. "
       # + two_players(Constants.multiplier_good, 'experimenter', Constants.multiplier_good, '') +
       'Conversely, if you choose to hide it, the <b>other player</b> will see your character hiding her/his multiplier'
       ' by means of a sign in the <b>contribution step</b>.<br>'
       '<br>Suppose you were attributed the <b style="color: #5893f6">blue</b> type and the other player the <b style="color: #d4c84d">yellow</b>'
       '. There are some possible scenarios below:<br><br>'
       '<b>1) You both disclose and the experimenter further reveals each of your multipliers</b> <br><br>' + two_players(Constants.multiplier_good, Constants.multiplier_bad,
                                                            Constants.multiplier_good, Constants.multiplier_bad) +
       '<b>2) You both hide</b> <br><br>' + two_players(None, None, '...', '...') +
       "<b>3) You both disclose and the experimenter reveals your partner's type to you but hides your type to your partner</b> <br><br>" + two_players(Constants.multiplier_good, None,
                                                                                  Constants.multiplier_good, '...') +
       "<b>4) You both disclose and the experimenter reveals your type to your partner but hides your partner's type to you</b> <br><br>" + two_players(None, Constants.multiplier_bad, '...',
                                                                                  Constants.multiplier_bad) +
       '<br><br><b> Please note that you have 30 seconds to choose to disclose or hide your multiplier, if you take more time, you will be disconnected.<br>'
       '<p>',

    4: '<p>'
       'In the second step of the round, you will see the outcome of the previous decision, such as the <b>scenarios</b> above.'
       '<br><br>Also, in each round, your private wallet  will be <b>endowed with 10 points</b>, and you will be asked to contribute to the public pot. You will be able to do so '
       'using a slider, which value corresponds to the number of points you want to put in the public pot. <br>'
       'To select a value on the slider you can either select with your mouse cursor, either using your left and right arrow keys on your keyboard.'
       ' The maximum contribution is 10, while the minimum is 0.<br>'
       '<br><div align="center"><img src="/static/img/contribute.gif"><br></div>'
       '<br><b> Please note that you have 30 seconds to give your contribution, if you take more time, you will be disconnected.<br>'
       '</p>',
    5: '<p>'
       'In the third step of the round, you will see the <b>outcome</b> of the <b>contribution step</b>. '
       'Your type, as well as the type of the player with whom you have played will be revealed.<br>'  
       f'<br><br>Suppose you are a <b style="color: #d4c84d">yellow</b> player, your contribution to the public pot will be multiplied by <b style="color: #d4c84d">{Constants.multiplier_bad}</b>. '
       f'Suppose you chose to contribute 10 points to the public pot, then your final contribution will be {Constants.multiplier_bad * 10} because 10x<b style="color: #d4c84d">{Constants.multiplier_bad}</b> = {Constants.multiplier_bad * 10}.<br>'
       '<br>Suppose the other player is <b style="color: #5893f6">blue</b> and chose to contribute also 10 points to the public pot, '
       f' then his/her final contribution will be {Constants.multiplier_good * 10} because 10x <b style="color: #5893f6">{Constants.multiplier_good}</b> = {Constants.multiplier_good * 10} <br>'
       '<br><br>The total contribution (the sum of both player contribution) is then distributed equally among the players such that:<br>'
       f'<div align="center">IND. SHARE = {(Constants.multiplier_good * 10 + Constants.multiplier_bad * 10) / 2} = ((10x<b style="color: #d4c84d">{Constants.multiplier_bad}</b>) + (10x<b style="color: #5893f6">{Constants.multiplier_good}</b>))/2</div>'
       f'<br>It means that both player individual share is {(Constants.multiplier_good * 10 + Constants.multiplier_bad * 10) / 2} points for this hypothetical round. <br><br>'
       '<b>Please note that the payoff you will receive is your individual share added to the points left in your private wallet. In the fictional example above, there are no points left '
       'in your private wallet because you contributed the maximum number of points.<b><br><br>'
       f'<b>Please note that payoffs from all the {Constants.num_rounds - 3} rounds are summed at the end of the experiment. This sum is used to compute your bonus compensation.'
       ' Also note that the first 3 training rounds are not used to compute your bonus.</b><br><br>'
       'Regarding your bonus compensation, here is the conversion: <br>'
       f' 1 point = {np.round(pounds_per_point * 100, 2)} pence <br>'
       f' 300 points =  {np.round(300 * pounds_per_point)} pound <br>'
       f'Note that you can win up to {np.round(pounds_per_point * 25 * (Constants.num_rounds - 3))} pound(s) as a bonus compensation.'
       '</p>',
    6: '<p>'
       '<br><br><b> The training game will start in time seconds.</b>'
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
