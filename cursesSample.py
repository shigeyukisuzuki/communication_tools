import curses

def main(stdscr):
	curses.curs_set(0)
	stdscr.clear()

	#display_widget = stdscr.subwin(curses.LINES - 2, curses.COLS, 0, 0)
	display_widget = curses.newpad(curses.LINES - 2, curses.COLS)
	display_widget.box()
	#display_widget.addstr(1, 1, "Display Widget")
	display_widget.refresh(0, 0, 0, 0, curses.LINES - 2, curses.COLS)

	input_widget = stdscr.subwin(1, curses.COLS, curses.LINES - 1, 0)
	#input_widget.box()
	input_widget.addstr(0, 1, "$ ")
	input_widget.refresh()

	input_string = ""
	numberOfLines = 0
	positionInRows = 0
	positionInLines = 0
	history = []

	while True:
		key = stdscr.getch()

		# Enterキーを押したら入力を表示用ウィジェットに追加し、入力をクリア
		if key == 10:  # 10はEnterキーのASCIIコード
			# qを押すと終了
			if input_string == 'quit':
				break
			numberOfLines += 1
			display_widget.addstr(numberOfLines, 1, input_string)
			display_widget.refresh(0, 0, 0, 0, curses.LINES - 2, curses.COLS)
			input_widget.addstr(0, 3, "_"*80)
			input_widget.refresh()
			history.append(input_string)
			input_string = ""  # 入力をクリア

			# 'quit'が入力されたら終了
			if history[-1] == 'quit':
				break

		# バックスペースキーを押したら入力を削除
		elif key == curses.KEY_BACKSPACE:
			if input_string:
				input_string = input_string[:-1]
			input_widget.addstr(0, 3, input_string + "_"*(80 - len(input_string)))
			input_widget.refresh()
		elif key == curses.KEY_DOWN:
			positionInLines += 1
			if positionInLines >= curses.LINES - 2:
				positionInLines = curses.LINES - 2 - 1
			display_widget.refresh(positionInLines, positionInRows, 0, 0, curses.LINES, curses.COLS)
		elif key == curses.KEY_UP:
			positionInLines -= 1
			if positionInLines < 0:
				positionInLines = 0
			display_widget.refresh(positionInLines, positionInRows, 0, 0, curses.LINES, curses.COLS)
		elif key == curses.KEY_LEFT:
			positionInRows -= 1
			if positionInRows < 0:
				positionInRows = 0
			display_widget.refresh(positionInLines, positionInRows, 0, 0, curses.LINES, curses.COLS)
		elif key == curses.KEY_RIGHT:
			positionInRows += 1
			if positionInRows >= curses.COLS:
				positionInRows = curses.COLS - 1
			display_widget.refresh(positionInLines, positionInRows, 0, 0, curses.LINES, curses.COLS)
		elif key == curses.KEY_HOME:
			positionInRows = 0
			display_widget.refresh(positionInLines, positionInRows, 0, 0, curses.LINES, curses.COLS)
		elif key == curses.KEY_PPAGE:
			positionInLines -= int(curses.LINES / 2)
			if positionInLines < 0:
				positionInLines = 0
			display_widget.refresh(positionInLines, positionInRows, 0, 0, curses.LINES, curses.COLS)
		elif key == curses.KEY_NPAGE:
			positionInLines += int(curses.LINES / 2)
			if positionInLines >= curses.LINES - 2:
				positionInLines = curses.LINES - 2 - 1
			display_widget.refresh(positionInLines, positionInRows, 0, 0, curses.LINES, curses.COLS)
		# それ以外の文字を入力用ウィジェットに追加
		else:
			input_string += chr(key)
			input_widget.addstr(0, 3, input_string)
			input_widget.refresh()

if __name__ == "__main__":
	curses.wrapper(main)

