# AICount
このプログラムはChatGPT3.5によって生成されました（ちょっとだけ手直しした）


各種設定の変更はconfig.iniを書き換えて変更可

[Settings]
reset_number
reset_number_2
 AI数を2パターン設定できる
 後述のchange_hotkeyで切り替え

count_hotkey
 AIカウントを増やすときのキー

change_hotkey = shift
 AI数のパターンを切り替えるためのキー


[AdditionalText]
display_additional_text = true
 AI数のパターンがどちらかを左に数字で表示するかどうか
 trueで表示、falseで非表示
 なんか実装が適当なせいでAI1のときにshiftで切り替えても切り替わらないがまあ気にしないで



※hotkeyにアルファベットキーや数字キー以外の特殊キーを設定したい場合

f1　： F1 キー （F12まで同様）
shift : Shift キー
ctrl : Ctrl キー
alt : Alt キー

backspace : バックスペースキー
tab : タブキー
enter : エンターキー
pause : Pause/Break キー
caps_lock : Caps Lock キー
esc : エスケープキー
space : スペースキー
page_up : Page Up キー
page_down : Page Down キー
end : End キー
home : Home キー
left : 左矢印キー
up : 上矢印キー
right : 右矢印キー
down : 下矢印キー
insert : Insert キー
delete : Delete キー
print_screen : Print Screen キー
