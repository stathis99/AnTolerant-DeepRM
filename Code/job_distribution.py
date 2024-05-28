import numpy as np


class Dist:

    def __init__(self, num_res, max_nw_size, job_len):
        self.num_res = num_res
        self.max_nw_size = max_nw_size
        self.job_len = job_len

        self.job_small_chance = 0.8

        self.job_len_big_lower = job_len * 2 / 3
        self.job_len_big_upper = job_len

        self.job_len_small_lower = 1
        self.job_len_small_upper = job_len / 5

        self.dominant_res_lower = max_nw_size / 2
        self.dominant_res_upper = max_nw_size

        self.other_res_lower = 1
        self.other_res_upper = max_nw_size / 5

    def normal_dist(self):

        # new work duration
        nw_len = np.random.randint(1, self.job_len + 1)  # same length in every dimension

        nw_size = np.zeros(self.num_res)

        for i in range(self.num_res):
            nw_size[i] = np.random.randint(1, self.max_nw_size + 1)

        return nw_len, nw_size

    def bi_model_dist(self):

        # -- job length --
        if np.random.rand() < self.job_small_chance:  # small job
            nw_len = np.random.randint(self.job_len_small_lower,
                                       self.job_len_small_upper + 1)
        else:  # big job
            nw_len = np.random.randint(self.job_len_big_lower,
                                       self.job_len_big_upper + 1)

        nw_size = np.zeros(self.num_res)

        # -- job resource request --
        dominant_res = np.random.randint(0, self.num_res)
        for i in range(self.num_res):
            if i == dominant_res:
                nw_size[i] = np.random.randint(self.dominant_res_lower,
                                               self.dominant_res_upper + 1)
            else:
                nw_size[i] = np.random.randint(self.other_res_lower,
                                               self.other_res_upper + 1)



        return nw_len, nw_size

    def bi_model_dist_anomalous(self):

        # mu_lenght = 1.5 
        # sigma_lenght = 0.4
        mu_res = 1.5

        #no anomalies
        sigma_res = 0.2 

        #mid anomalies
        #sigma_res = 0.5 

        #large anomalies

        
        # -- job length --
        if np.random.rand() < self.job_small_chance:  # small job
            nw_len = np.random.randint(self.job_len_small_lower,
                                       self.job_len_small_upper + 1)
        else:  # big job
            nw_len = np.random.randint(self.job_len_big_lower,
                                       self.job_len_big_upper + 1)

        nw_size = np.zeros(self.num_res)

        # -- job resource request --
        dominant_res = np.random.randint(0, self.num_res)
        for i in range(self.num_res):
            if i == dominant_res:
                nw_size[i] = np.round(np.random.lognormal(mu_res, sigma_res, 1)).astype(int)
            else:
                nw_size[i] = np.round(np.random.lognormal(mu_res, sigma_res, 1)).astype(int)


        return nw_len, nw_size    

def print_info_about_jobs(pa,nw_len_seqs,nw_size_seqs):
    count = 0
    total = len(nw_size_seqs)

    print pa.res_slot
    for job in nw_size_seqs:
        if np.any(job > pa.res_slot):
            count += 1

    percentage = (count / total) * 100
    print "----------------------------------------percentage of anomalies : ", count,"/", total 

def generate_sequence_work(pa, seed=42):

    np.random.seed(seed)

    simu_len = pa.simu_len * pa.num_ex

    nw_dist = pa.dist.bi_model_dist_anomalous



    nw_len_seq = np.zeros(simu_len, dtype=int)
    nw_size_seq = np.zeros((simu_len, pa.num_res), dtype=int)

    for i in range(simu_len):

        if np.random.rand() < pa.new_job_rate:  # a new job comes

            nw_len_seq[i], nw_size_seq[i, :] = nw_dist()

    print_info_about_jobs(pa,nw_len_seq,nw_size_seq)


    nw_len_seq = np.reshape(nw_len_seq,
                            [pa.num_ex, pa.simu_len])
    nw_size_seq = np.reshape(nw_size_seq,
                             [pa.num_ex, pa.simu_len, pa.num_res])
        
        

    #print nw_len_seq
    #print nw_size_seq


    return nw_len_seq, nw_size_seq
