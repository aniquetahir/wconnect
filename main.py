import urwid
import subprocess

palette = [
    ('banner', 'black', 'light gray'),
    ('prompt', 'white', 'dark gray'),
    ('bg', 'black', 'dark blue'),
    ('reversed', 'standout', ''),]


# Get interface name
def get_interface_names():
    command = "ifconfig -a | sed 's/[ \\t].*//;/^$/d'"
    result = subprocess.run(command, shell=True,stdout=subprocess.PIPE)
    interfaces = result.stdout
    interfaces = [x.strip().replace(':', '') for x in interfaces.decode('utf-8').split('\n') if ':' in x]
    return interfaces

def get_ssids(interface):
    print("Scanning...")
    try:
        if interface.strip() == '':
            import sys
            print('Invalid interface selected', file=sys.stderr)
            exit(0)
        command = 'sudo iw "%s" scan | grep SSID:' % interface  # TODO Possible vulnerability (fix)
        result = subprocess.run(command, shell=True,stdout=subprocess.PIPE)
        ssids = result.stdout
        ssids = [x.replace('SSID:', '').strip() for x in ssids.decode('utf-8').split('\n')]
        ssids = [x for x in ssids if x is not '']
        print("----=====SSIDS=====-----")
        print(ssids)
        if not ssids or len(ssids)==0:
            print('No SSIDS detected')
            exit()
        return ssids
    except Exception as err:
        print(err)
        exit(0)


def connect_network(button):
    password = password_widget.get_edit_text()
    main_loop.stop()
    command = 'sudo iwconfig "%s" essid "%s" key "%s"' % (chosen_interface, chosen_ssid, password)
    print("Running command:\n%s" % command)
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(result.stdout)
    print(result.stderr)
    exit(result.returncode)

interface_names = get_interface_names()
chosen_interface = None
chosen_ssid = None
chosen_password = None


def menu(title, choices, chosen_fn):
    body = [urwid.Text(title), urwid.Divider()]
    for c in choices:
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', chosen_fn, c)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def ssid_widget(ssids):
    main = urwid.Padding(menu(u'Select SSID:', ssids), left=2, right=2)
    top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                        align='center', width=('relative', 60),
                        valign='middle', height=('relative', 60),
                        min_width=20, min_height=9)
    return top

def interface_selection_menu():
    main = urwid.Padding(menu(u'Select an Interface:', interface_names, on_interface_chosen), left=2, right=2)
    main = urwid.AttrMap(main, 'banner')
    top = urwid.Overlay(main, urwid.SolidFill(u' '),
                        align='center', width=('relative', 60),
                        valign='middle', height=('relative', 60),
                        min_width=20, min_height=9)
    return urwid.AttrMap(top, 'bg')

def ssid_selection_menu():
    ssids = get_ssids(chosen_interface)
    main = urwid.Padding(menu(u'Select SSID:', ssids, on_ssid_chosen), left=2, right=2)
    main = urwid.AttrMap(main, 'banner')
    top = urwid.Overlay(main, urwid.SolidFill(u' '),
                        align='center', width=('relative', 60),
                        valign='middle', height=('relative', 60),
                        min_width=20, min_height=9)
    return urwid.AttrMap(top, 'bg')

password_widget = None

def password_menu():
    global password_widget
    password_prompt = urwid.Text("Password: ", align='center')
    password_widget = urwid.Edit("", align='center', mask='*')
    txt_password = urwid.AttrMap(password_widget, 'prompt')
    btn_ok = urwid.Button('Ok')
    btn_cancel = urwid.Button('Cancel')


    urwid.connect_signal(btn_cancel, 'click', exit_program)
    urwid.connect_signal(btn_ok, 'click', connect_network)


    filler = urwid.Filler(
        urwid.Pile([
            password_prompt,
            txt_password,
            urwid.AttrMap(btn_ok, None, 'reversed'),
            urwid.AttrMap(btn_cancel, None, 'reversed')
        ]))
    padding = urwid.Padding(filler, left=2, right=2)

    ppadding = urwid.AttrMap(padding, 'banner')
    # prompt = urwid.Edit(u"Password", mask=u'*')
    top = urwid.Overlay(ppadding, urwid.SolidFill(u' '),
                        align='center', width=('relative', 60),
                        valign='middle', height=('relative', 60),
                        min_width=20, min_height=9)
    topp = urwid.AttrMap(top, 'bg')
    return topp

def on_ssid_chosen(button, choice):
    '''
    This function handles the user choice when an SSID is chosen i.e. password selection screen

    :param button:
    :param choice:
    :return:
    '''
    global chosen_ssid
    chosen_ssid = choice

    global main_loop
    main_loop.stop()

    main_loop = urwid.MainLoop(password_menu(), palette)
    main_loop.run()

def on_interface_chosen(button, choice):
    # done = urwid.Button(u'Ok')
    # urwid.connect_signal(done, 'click', exit_program)
    global chosen_interface
    chosen_interface = choice

    global main_loop
    main_loop.stop()
    main_loop = urwid.MainLoop(ssid_selection_menu(), palette)
    main_loop.run()

def exit_program(button):
    exit()
    # raise urwid.ExitMainLoop()

ism = interface_selection_menu()
main_loop = urwid.MainLoop(ism, palette)
main_loop.run()