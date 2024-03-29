#! /bin/sh

#-------------------------------------------------------------------
# 脚本参数
#-------------------------------------------------------------------


# 程序名称
MODEL_NAME=CAT_GPON

# 类路径
MODEL_LIBS=`ls ../lib/*.jar | paste -s -d":" -`

# JAVA运行环境参数
MODEL_OPTS="-server -d64 -Xms1g -Xmx256g -Xmn6g -XX:SurvivorRatio=65536 -XX:+UseBiasedLocking -XX:+DisableExplicitGC -XX:MaxTenuringThreshold=0 -XX:+UseConcMarkSweepGC -XX:+UseParNewGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -XX:CMSFullGCsBeforeCompaction=0 -XX:CMSInitiatingOccupancyFraction=70 -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly"

# 执行类
MODEL_CLASS="com.eastcom.cat.v20.Application"

# 程序参数
MODEL_VARS=

# 是否后台运行
MODEL_DAEMON=1

# 控制台日志
MODEL_LOG="../logs/error.log"


#----------------------------------------------------------
# 固定内容
#----------------------------------------------------------

SLEEP_MIN=5

# model info can be define here
MODEL_SYMBOL=${MODEL_NAME}
GREP_KEY="Diname="${MODEL_SYMBOL}

# CLASSPATH can bu define here
CLASSPATH=.:../conf/:${MODEL_LIBS}:.:${CLASSPATH}


#----------------------------------------------------------
# function print usage
#----------------------------------------------------------

print_usage()
{
echo ""
echo "\th|H|help|HELP             \tPrint help information."
echo "\tstart                     \tStart the ${MODEL_NAME} server."
echo "\tstop                      \tStop the ${MODEL_NAME} server."
echo "\tstatus                    \tStatus the ${MODEL_NAME} server."
}

#-------------------------------------------------------------------
# function model_is_exist
#-------------------------------------------------------------------

modelService_is_exist()
{
localServerId=`ps -ef |grep "${GREP_KEY}" | grep -v grep | awk '{print $2}'`
if [ -z "${localServerId}" ]
then
return 1
else
return 0
fi
}

#-------------------------------------------------------------------
# function check_user_id
# return 0 ---- supper user
# return 1 ---- normal user
#-------------------------------------------------------------------

# check_user_id ()
# {
# localMyId=$(id|awk '{print $1}')
# localMyId=${localMyId:4:1}
# if [ "${localMyId}" -eq "0" ]
# then
# return 0
# else
# return 1
# fi
# }

#-------------------------------------------------------------------
# function model_start
#-------------------------------------------------------------------

model_start ()
{
modelService_is_exist

if [ $? -eq "0" ]
then
echo "${MODEL_NAME} is running yet. pid ${localServerId}."
return 0
else
if [ $MODEL_DAEMON = 0 ]
then
echo "try to start ${MODEL_NAME} ... foreground"
$JAVA_HOME/bin/java -${GREP_KEY} -classpath ${CLASSPATH} ${MODEL_OPTS} ${MODEL_CLASS} ${MODEL_VARS}
else
echo "try to start ${MODEL_NAME} ... backgroud"
nohup $JAVA_HOME/bin/java -${GREP_KEY} ${MODEL_OPTS} -classpath ${CLASSPATH} ${MODEL_CLASS} ${MODEL_VARS} 1>&- 2>>${MODEL_LOG} &
sleep $SLEEP_MIN
modelService_is_exist
if [ $? -eq "0" ]
then
echo "${MODEL_NAME} is running now. pid ${localServerId}."
return 0
else
echo "failed to start ${MODEL_NAME}! see the output log for more details."
return 1
fi
fi
fi
}

#-------------------------------------------------------------------
# function model_stop
#-------------------------------------------------------------------

model_stop()
{
echo "try to stop ${MODEL_NAME} ..."
modelService_is_exist

if [ $? -eq 0 ]
then
/usr/bin/kill -9 ${localServerId}
if [ $? -ne 0 ]
then
echo "failed to stop ${MODEL_NAME}!"
return 1
else
echo "${MODEL_NAME} stopped."
return 0
fi
else
echo "${MODEL_NAME} is not running!"
return 1
fi
}

#-------------------------------------------------------------------
# function model_status
#-------------------------------------------------------------------

model_status()
{
modelService_is_exist
if [ $? -eq 0 ]
then
echo "${MODEL_NAME} is running. pid ${localServerId}."
else
echo "${MODEL_NAME} is not running."
fi
}

#-------------------------------------------------------------------
#
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# function parse_para
#-------------------------------------------------------------------

parse_para()
{
case "$1" in
start) model_start;;
stop) model_stop;;
status) model_status;;
*) echo "illage parameter : $1";print_usage;;
esac
}

#-------------------------------------------------------------------
# main
#-------------------------------------------------------------------

parse_para $1

