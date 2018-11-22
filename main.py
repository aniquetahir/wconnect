import urwid
import subprocess

# Get interface name
def get_interface_names():
    command = "ifconfig -a | sed 's/[ \\t].*//;/^$/d'"
    result = subprocess.run(command, shell=True,stdout=subprocess.PIPE)
    interfaces = result.stdout
    interfaces = [x.strip().replace(':', '') for x in interfaces.decode('utf-8').split('\n') if ':' in x]
    return interfaces

def get_ssids():
    command = "ifconfig -a | sed 's/[ \\t].*//;/^$/d'"
    result = subprocess.run(command, shell=True,stdout=subprocess.PIPE)
    interfaces = result.stdout
    interfaces = [x.strip().replace(':', '') for x in interfaces.decode('utf-8').split('\n') if ':' in x]
    return interfaces

interface_names = get_interface_names()
ssids = []

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


def interface_chosen(button, choice):
    response = urwid.Text([u'You chose ', choice, u'\n'])
    done = urwid.Button(u'Ok')
    urwid.connect_signal(done, 'click', exit_program)
    main.original_widget = urwid.Filler(urwid.Pile([response,
        urwid.AttrMap(done, None, focus_map='reversed')]))

def exit_program(button):
    raise urwid.ExitMainLoop()

main = urwid.Padding(menu(u'Select an Interface:', interface_names, interface_chosen), left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 60),
    valign='middle', height=('relative', 60),
    min_width=20, min_height=9)
urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()