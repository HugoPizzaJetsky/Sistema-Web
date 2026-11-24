[Setup]
AppName=RDB Digital
AppVersion=1.0
AppPublisher=RDB Digital
PrivilegesRequired=lowest
DefaultDirName={autopf}\RDBDigital
DefaultGroupName=RDB Digital
OutputDir=..\instalador
OutputBaseFilename=Instalador_RDB_Digital
Compression=lzma
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\RDBDigital.exe

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar um atalho na Área de Trabalho"; GroupDescription: "Atalhos adicionais:"

[Files]
Source: "..\dist\RDBDigital\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\RDB Digital"; Filename: "{app}\RDBDigital.exe"
Name: "{group}\Desinstalar RDB Digital"; Filename: "{uninstallexe}"
Name: "{autodesktop}\RDB Digital"; Filename: "{app}\RDBDigital.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\RDBDigital.exe"; Description: "Abrir o RDB Digital agora"; Flags: nowait postinstall skipifsilent
