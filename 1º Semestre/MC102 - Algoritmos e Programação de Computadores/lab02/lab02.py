print('Este é um sistema que irá te ajudar a escolher a sua próxima Distribuição Linux. '
      'Responda a algumas poucas perguntas para ter uma recomendação.')

def show_error():
    print('Opção inválida, recomece o questionário.')
    exit()

def ask_question(question, is_dev_question=False):
    if is_dev_question:
        answer = int(input(f'{question}\n(0) Não\n(1) Sim\n(2) Sim, realizo testes e invasão de sistemas\n'))

        if answer not in [0, 1, 2]:
            show_error()
    else:
        answer = int(input(f'{question}\n(0) Não\n(1) Sim\n'))

        if answer not in [0, 1]:
            show_error()

    return answer

def show_result(path, distros):
    if path == 'aprendizado':
        print(f'Ao trilhar esse caminho, um novo guru do Linux irá surgir, as distribuições que servirão de base para seu aprendizado são: {", ".join(distros)}.')
    elif path == 'desafios':
        print(f'Suas escolhas te levaram a um caminho repleto de desafios, para você recomendamos as distribuições: {", ".join(distros)}.')
    elif path == 'motivacao':
        print(f'Você passará pelo caminho daqueles que decidiram abandonar sua zona de conforto, as distribuições recomendadas são: {", ".join(distros)}.')


if ask_question('Seu SO anterior era Linux?') == 1:
    is_dev = ask_question('É programador/ desenvolvedor ou de áreas semelhantes?', True)

    if is_dev == 0:
        show_result('aprendizado', ['Ubuntu Mint', 'Fedora'])

    elif is_dev == 1:
        if ask_question('Gostaria de algo pronto para uso ao invés de ficar configurando o SO?') == 1:
            if ask_question('Já utilizou Debian ou Ubuntu?') == 1:
                show_result('desafios', ['Manjaro, ApricityOS'])
            else:
                show_result('aprendizado', ['OpenSuse, Ubuntu Mint, Ubuntu Mate, Ubuntu'])
            
        else:
            if ask_question('Já utilizou Arch Linux?') == 1:
                show_result('desafios', ['Gentoo', 'CentOS', 'Slackware'])
            else:
                show_result('aprendizado', ['Antergos', 'Arch Linux'])

    elif is_dev == 2:
        show_result('aprendizado', ['Kali Linux', 'Black Arch'])

    else:
        show_error()

else:
    if ask_question('Seu SO anterior era um MacOS?') == 1:
        show_result('motivacao', ['ElementaryOS', 'ApricityOS'])
    else:
        show_result('motivacao', ['Ubuntu Mate', 'Ubuntu Mint', 'Kubuntu', 'Manjaro'])