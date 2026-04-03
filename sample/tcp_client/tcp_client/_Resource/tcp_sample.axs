PROGRAM_NAME='udp_sample'
(***********************************************************)
(***********************************************************)
(*  FILE_LAST_MODIFIED_ON: 04/05/2006  AT: 09:00:25        *)
(***********************************************************)
(* System Type : NetLinx                                   *)
(***********************************************************)
(* REV HISTORY:                                            *)
(***********************************************************)
(*
    $History: $
*)
(***********************************************************)
(*          DEVICE NUMBER DEFINITIONS GO BELOW             *)
(***********************************************************)
DEFINE_DEVICE

dvIP	= 0:4:0
dvTP	= 10001:1:0

(***********************************************************)
(*               CONSTANT DEFINITIONS GO BELOW             *)
(***********************************************************)
DEFINE_CONSTANT

IP_RECV_PORT	= 10000

(***********************************************************)
(*              DATA TYPE DEFINITIONS GO BELOW             *)
(***********************************************************)
DEFINE_TYPE

(***********************************************************)
(*               VARIABLE DEFINITIONS GO BELOW             *)
(***********************************************************)
DEFINE_VARIABLE

long	lTL[] = {300}

VOLATILE integer isOnline

(***********************************************************)
(*               LATCHING DEFINITIONS GO BELOW             *)
(***********************************************************)
DEFINE_LATCHING

(***********************************************************)
(*       MUTUALLY EXCLUSIVE DEFINITIONS GO BELOW           *)
(***********************************************************)
DEFINE_MUTUALLY_EXCLUSIVE

(***********************************************************)
(*        SUBROUTINE/FUNCTION DEFINITIONS GO BELOW         *)
(***********************************************************)
(* EXAMPLE: DEFINE_FUNCTION <RETURN_TYPE> <NAME> (<PARAMETERS>) *)
(* EXAMPLE: DEFINE_CALL '<NAME>' (<PARAMETERS>) *)

(***********************************************************)
(*                STARTUP CODE GOES BELOW                  *)
(***********************************************************)
DEFINE_START

TIMELINE_CREATE(1,lTL,1,TIMELINE_ABSOLUTE,TIMELINE_REPEAT)

(***********************************************************)
(*                THE EVENTS GO BELOW                      *)
(***********************************************************)
DEFINE_EVENT

TIMELINE_EVENT [1]
{
    [dvTP,3] = isOnline
}

DATA_EVENT [dvIP]
{
    ONLINE:
	isOnline = TRUE
    OFFLINE:
	isOnline = FALSE
    STRING:
	SEND_COMMAND dvTP,"'^TXT-1,0,',DATA.TEXT"
}

BUTTON_EVENT [dvTP,1]
{
    PUSH:
    {
	TO[BUTTON.INPUT]
	
	IP_SERVER_OPEN(dvIP.PORT,IP_RECV_PORT,IP_TCP)
    }
}
BUTTON_EVENT [dvTP,2]
{
    PUSH:
    {
	TO[BUTTON.INPUT]
	
	IP_SERVER_CLOSE(dvIP.PORT)
    }
}
BUTTON_EVENT [dvTP,4]
{
    PUSH:
    {
	TO[BUTTON.INPUT]
	
	SEND_STRING dvIP,'Hello, world!'
    }
}
BUTTON_EVENT [dvTP,5]
{
    PUSH:
    {
	TO[BUTTON.INPUT]
	
	SEND_STRING dvIP,'XYZ'
    }
}
BUTTON_EVENT [dvTP,6]
{
    PUSH:
    {
	TO[BUTTON.INPUT]
	
	SEND_COMMAND dvTP,'^TXT-1,0,'
    }
}


(*****************************************************************)
(*                                                               *)
(*                      !!!! WARNING !!!!                        *)
(*                                                               *)
(* Due to differences in the underlying architecture of the      *)
(* X-Series masters, changing variables in the DEFINE_PROGRAM    *)
(* section of code can negatively impact program performance.    *)
(*                                                               *)
(* See “Differences in DEFINE_PROGRAM Program Execution” section *)
(* of the NX-Series Controllers WebConsole & Programming Guide   *)
(* for additional and alternate coding methodologies.            *)
(*****************************************************************)

DEFINE_PROGRAM

(*****************************************************************)
(*                       END OF PROGRAM                          *)
(*                                                               *)
(*         !!!  DO NOT PUT ANY CODE BELOW THIS COMMENT  !!!      *)
(*                                                               *)
(*****************************************************************)


