import numpy as np



def bi_model_dist(num_res, max_nw_size, job_len):
    num_res = num_res
    max_nw_size = max_nw_size
    job_len = job_len

    job_small_chance = 0.8

    job_len_big_lower = job_len * 2 / 3
    job_len_big_upper = job_len

    job_len_small_lower = 1
    job_len_small_upper = job_len / 5

    dominant_res_lower = max_nw_size / 2
    dominant_res_upper = max_nw_size

    other_res_lower = 1
    other_res_upper = max_nw_size / 5

    # -- job length --
    if np.random.rand() < job_small_chance:  # small job
        nw_len = np.random.randint(job_len_small_lower,
                                    job_len_small_upper + 1)
    else:  # big job
        nw_len = np.random.randint(job_len_big_lower,
                                    job_len_big_upper + 1)

    nw_size = np.zeros(num_res)

    # -- job resource request --
    dominant_res = np.random.randint(0, num_res)
    for i in range(num_res):
        if i == dominant_res:
            nw_size[i] = np.random.randint(dominant_res_lower,
                                            dominant_res_upper + 1)
        else:
            nw_size[i] = np.random.randint(other_res_lower,
                                            other_res_upper + 1)

    return nw_len, nw_size    


    
def generate_sequence_work(simu_len):

    nw_len_seq = np.zeros(simu_len, dtype=int)
    nw_size_seq = np.zeros((simu_len, 2), dtype=int)

    for i in range(simu_len):

        if np.random.rand() < 0.7:  # a new job comes

            nw_len_seq[i], nw_size_seq[i, :] = bi_model_dist(2,10,15)

    return nw_len_seq, nw_size_seq


def launch(pa):

    print("Anomaly detection !")
    print("Jobs to be generated :", pa.simu_len * pa.num_ex)
    nw_len_seqs, nw_size_seqs = generate_sequence_work(pa.simu_len * pa.num_ex)
    print(nw_len_seqs)
    print(nw_size_seqs)
    print("done !")
