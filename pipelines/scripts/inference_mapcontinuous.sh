dm-getsplit -r ~/studium/BA_EXPERIMENTS/corpus/ -s test | dm-mapcommand-bulk -r ~/studium/BA_EXPERIMENTS/corpus/ -a dDoc_inference_data -o dDoc_T1000_inference_result -c "~/studium/tools/plda/infer --alpha 0.1 --beta 0.01 --inference_data_file /dev/stdin --inference_result_file >(cat) --model_file ~/studium/BA_EXPERIMENTS/components/LDA/dDoc/T1000/dDoc_T1000.plda_model --total_iterations 2000 --burn_in_iterations 1500" -I "
" -O "
" --overwrite & \
dm-getsplit -r ~/studium/BA_EXPERIMENTS/corpus/ -s dev | dm-mapcommand-bulk -r ~/studium/BA_EXPERIMENTS/corpus/ -a dDoc_inference_data -o dDoc_T1000_inference_result -c "~/studium/tools/plda/infer --alpha 0.1 --beta 0.01 --inference_data_file /dev/stdin --inference_result_file >(cat) --model_file ~/studium/BA_EXPERIMENTS/components/LDA/dDoc/T1000/dDoc_T1000.plda_model --total_iterations 2000 --burn_in_iterations 1500" -I "
" -O "
" --overwrite & \
dm-getsplit -r ~/studium/BA_EXPERIMENTS/corpus/ -s test | dm-mapcommand-bulk -r ~/studium/BA_EXPERIMENTS/corpus/ -a dImg_750_inference_data -o dImg_K750_T1000_inference_result -c "~/studium/tools/plda/infer --alpha 0.1 --beta 0.01 --inference_data_file /dev/stdin --inference_result_file >(cat) --model_file ~/studium/BA_EXPERIMENTS/components/LDA/dImg/K750/T1000/dImg_K750_T1000.plda_model --total_iterations 2000 --burn_in_iterations 1500" -I "
" -O "
" --overwrite & \
dm-getsplit -r ~/studium/BA_EXPERIMENTS/corpus/ -s dev | dm-mapcommand-bulk -r ~/studium/BA_EXPERIMENTS/corpus/ -a dImg_750_inference_data -o dImg_K750_T1000_inference_result -c "~/studium/tools/plda/infer --alpha 0.1 --beta 0.01 --inference_data_file /dev/stdin --inference_result_file >(cat) --model_file ~/studium/BA_EXPERIMENTS/components/LDA/dImg/K750/T1000/dImg_K750_T1000.plda_model --total_iterations 2000 --burn_in_iterations 1500" -I "
" -O "
" --overwrite & \
dm-getsplit -r ~/studium/BA_EXPERIMENTS/corpus/ -s test | dm-mapcommand-bulk -r ~/studium/BA_EXPERIMENTS/corpus/ -a dMix_750_inference_data -o dMix_K750_T1000_inference_result -c "~/studium/tools/plda/infer --alpha 0.1 --beta 0.01 --inference_data_file /dev/stdin --inference_result_file >(cat) --model_file ~/studium/BA_EXPERIMENTS/components/LDA/dMix/K750/T1000/dMix_K750_T1000.plda_model --total_iterations 2000 --burn_in_iterations 1500" -I "
" -O "
" --overwrite & \
dm-getsplit -r ~/studium/BA_EXPERIMENTS/corpus/ -s dev | dm-mapcommand-bulk -r ~/studium/BA_EXPERIMENTS/corpus/ -a dMix_750_inference_data -o dMix_K750_T1000_inference_result -c "~/studium/tools/plda/infer --alpha 0.1 --beta 0.01 --inference_data_file /dev/stdin --inference_result_file >(cat) --model_file ~/studium/BA_EXPERIMENTS/components/LDA/dMix/K750/T1000/dMix_K750_T1000.plda_model --total_iterations 2000 --burn_in_iterations 1500" -I "
" -O "
" --overwrite
