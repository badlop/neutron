#$ neutron_plugin 01
# parts of code: Gh0st AKA Bohdan Turkynewych.

def admin_groupchat_invite_handler(source, groupchat, body):
	if has_access(source, COMMANDS['!join']['access']):
		join_groupchat(groupchat)

def handler_admin_join(type, source, parameters):
	if parameters:
		if len(string.split(parameters)) > 1:
			(groupchat, nick) = string.split(parameters.lstrip(), ' ', 1)
		else:
			groupchat = parameters.strip()
			nick = DEFAULT_NICK
		smsg(type, source, 'Joined ' + groupchat)
		join_groupchat(groupchat, nick)
	else:
		smsg(type, source, 'Invalid Syntax')

def handler_admin_leave(type, source, parameters):
	if len(string.split(parameters)) > 0:
		groupchat = parameters.strip()
	else:
		groupchat = source[1]
	leave_groupchat(groupchat)
	smsg(type, source, 'Left ' + groupchat)


def handler_admin_msg(type, source, parameters):
	msg(string.split(parameters)[0], string.join(string.split(parameters)[1:]))
	smsg(type, source, 'Message Sent')

def handler_admin_say(type, source, parameters):
	if parameters:
		msg(source[1], parameters)
	else:
		smsg(type, source, 'Enter Message')

def handler_admin_restart(type, source, parameters):
	#os.startfile(sys.argv[0])
	smsg(type, source, 'Restarting')
	print printc(color_bright_red, 'Received !restart from remote.')
	JCON.disconnect()
	os.execv('./neutron.py', sys.argv)

def handler_admin_exit(type, source, parameters):
	#os.startfile(sys.argv[0])
	smsg(type, source, 'Exiting')
	print printc(color_bright_red, 'Received !exit from remote.')
	JCON.disconnect()
	os.abort()


def t_conv(timestamp):
	reply = ''
	seconds = timestamp % 60
	minutes = (timestamp / 60) % 60
	hours = (timestamp / 3600) % 60
	days = timestamp / 216000
	if days: reply += str(days) + 'd '
	if hours: reply += str(hours) + 'h '
	if minutes: reply += str(minutes) + 'm '
	reply += str(seconds) + 's'
	return reply
    
def handler_admin_uptime(type, source, parameters):
	if BOOTUP_TIMESTAMP:
		idletime = int(time.time() - BOOTUP_TIMESTAMP)
		reply = 'Neutron bot is up for: ' + t_conv(idletime)
	else:
		reply = 'Unknown'
	smsg(type, source, reply)

def handler_admin_rooms(type, source, parameters):
	initialize_file(GROUPCHAT_CACHE_FILE, '[]')
	groupchats = eval(read_file(GROUPCHAT_CACHE_FILE))
        reply = '\nTotal Rooms: '+ str(len(groupchats)) + '\n' + '\n'.join(groupchats)
	smsg(type, source, reply)


def handler_admin_rejoinall(type, source, parameters):
	initialize_file(GROUPCHAT_CACHE_FILE, '[]')
	groupchats = eval(read_file(GROUPCHAT_CACHE_FILE))
	smsg(type, source, 'Rejoining *ALL* groupchats.')
	for groupchat in groupchats:
		leave_groupchat(groupchat)
		time.sleep(0.5)
		join_groupchat(groupchat)

def handler_admin_histclean(type, source, parameters):
	i = 0
	dots = 20
	dot = '.'
	room_sleep = 1.3
	if type == 'public':
	    while i <= dots:
	    	msg(source[1], dot)
		time.sleep(room_sleep)
		i += 1
	else:
	    smsg(type, source, 'Applicable to rooms only.')    

def admin_crashlog():
	initialize_file('crash.log','')
	data = read_file('crash.log')
	if data.strip():
	    data = 'Last crashlog:\n\n' + data
	    admin_bcast(data)

def admin_bcast(message):
    # This function sends message to all of botadmins,
    # as mentioned in config.txt
    # useful for debugging purposes.
    if message.strip():
	for admin in ADMINS:
	    msg(admin.strip(), message)
    

if __name__ == "__main__":
	# Notify bot admins with
	# last crashlog file.
	admin_crashlog()		

register_command_handler(handler_admin_join, '!join', 100, 'Joins specified groupchat.', '!join <groupchat> [nick]', ['!join jabber@conference.jabber.org', '!join jdev@conference.jabber.org neutron2'])
register_command_handler(handler_admin_leave, '!leave', 100, 'Joins specified (or current) groupchat.', '!leave [groupchat]', ['!leave jabber@conference.jabber.org', '!leave'])
register_command_handler(handler_admin_msg, '!msg' ,100, 'Sends a message to specified JID.', '!msg <jid> <message>', ['!msg mikem@jabber.org hey mike!'])
register_command_handler(handler_admin_say, '!say', 100, 'Sends a message to current groupchat or to your JID if message is not through groupchat.', '!say <message>', ['!say hi'])
register_command_handler(handler_admin_restart, '!restart', 100, 'Restarts me.', '!restart', ['!restart'])
register_command_handler(handler_admin_histclean, '!hclean', 0, 'Cleans room history using some string.', '!hclean', ['!hclean'])
register_command_handler(handler_admin_exit, '!exit', 100, 'Exits completely.', '!exit', ['!exit'])
register_command_handler(handler_admin_uptime, '!uptime', 0, 'Returns Neutron uptime.', '!uptime', ['!uptime'])
register_command_handler(handler_admin_rooms, '!rooms', 100, 'Returns Neutron\'s rooms.', '!rooms', ['!rooms'])
register_command_handler(handler_admin_rejoinall, '!rejoinall', 100, 'Rejoins *ALL* Neutron\'s rooms.', '!rejoinall', ['!rejoinall'])

register_groupchat_invite_handler(admin_groupchat_invite_handler)
