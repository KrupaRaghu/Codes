get_filter_pos ()
{
dm-getsplit -r ${CORPUS} -s "$1" | dm-itemfilterbyattr -r ${CORPUS} -a "$2" --pos
}
get_filter_neg ()
{
dm-getsplit -r ${CORPUS} -s "$1" | dm-itemfilterbyattr -r ${CORPUS} -a "$2" --neg
}
map_py ()
{
parallel --progress -N 1 --pipe --round-robin -j 8 dm-mappyfunc -r ${CORPUS} -m "$1" -f "$2" -a in_attr="$3",out_attr="$4"
}
map_cmd ()
{
parallel --progress -N 1 --pipe --round-robin -j 8 dm-mapcommand -r ${CORPUS} -c "$1" -a "$2" -o "$3" --print-reasons
}
map_files ()
{
    files=`find $2 -type f -name $3`
    for f in $files;
    do
        export DIR=$(dirname ${f})
        @$1 $f > $DIR/$4
    done
}
