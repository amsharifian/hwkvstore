### design, shared, root, local, lroot, launch
echo "qsub -v CONFIG=$1,SHARED=`hostname`:$2,ROOT=$3,LOCAL=$4,LROOT=$5,RISCV=$6 $7"
qsub -v CONFIG=$1,SHARED=`hostname`:$2,ROOT=$3,LOCAL=$4,LROOT=$5,RISCV=$6 $7
