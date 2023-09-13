sheila_choice = input()
reginaldo_choice = input()

if sheila_choice == reginaldo_choice:
    print('empate')
elif sheila_choice == 'tesoura' and reginaldo_choice in ['papel', 'lagarto']:
    print('Interestelar')
elif sheila_choice == 'papel' and reginaldo_choice in ['pedra', 'spock']:
    print('Interestelar')
elif sheila_choice == 'pedra' and reginaldo_choice in ['lagarto', 'tesoura']:
    print('Interestelar')
elif sheila_choice == 'lagarto' and reginaldo_choice in ['spock', 'papel']:
    print('Interestelar')
elif sheila_choice == 'spock' and reginaldo_choice in ['tesoura', 'pedra']:
    print('Interestelar')
else:
    print('Jornada nas Estrelas')
