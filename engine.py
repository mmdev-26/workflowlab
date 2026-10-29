"""Seeded multi-server tandem-queue discrete-event simulation.
Stages process jobs FCFS; one shared arrival stream permits paired comparisons.
"""
import heapq,math,random,statistics

def percentile(values,p):
    s=sorted(values);return s[max(0,math.ceil(len(s)*p)-1)] if s else 0

def simulate(arrivals,stages,seed):
    rng=random.Random(seed);times=list(arrivals);totals=[0.]*len(times);reports=[];all_waits=[0.]*len(times)
    names=set()
    for stage in stages:
        name=stage['name'];capacity=stage['servers'];mean=float(stage['serviceMean']);variation=stage.get('distribution','constant')
        if name in names:raise ValueError('Stage names must be unique')
        names.add(name)
        if not isinstance(capacity,int) or isinstance(capacity,bool) or not 1<=capacity<=1000:raise ValueError('servers must be an integer between 1 and 1000')
        if not math.isfinite(mean) or mean<=0:raise ValueError('serviceMean must be positive and finite')
        if variation not in ['constant','exponential']:raise ValueError('Unsupported service distribution')
        heap=[(0.,i) for i in range(capacity)];heapq.heapify(heap);departures=[0.]*len(times);waits=[];busy=0
        # Later stages must reorder jobs by their actual arrival times.
        for job in sorted(range(len(times)),key=lambda i:(times[i],i)):
            ready,server=heapq.heappop(heap);start=max(ready,times[job]);wait=start-times[job];service=mean if variation=='constant' else rng.expovariate(1/mean);end=start+service
            departures[job]=end;totals[job]+=service;all_waits[job]+=wait;waits.append(wait);busy+=service;heapq.heappush(heap,(end,server))
        horizon=max(departures)-min(times)
        reports.append({'name':name,'servers':capacity,'meanWait':statistics.mean(waits),'p95Wait':percentile(waits,.95),'busyTime':busy,'utilization':busy/(horizon*capacity) if horizon else 0})
        times=departures
    duration=[end-start for end,start in zip(times,arrivals)]
    return {'summary':{'jobs':len(times),'meanCycle':statistics.mean(duration),'p95Cycle':percentile(duration,.95),'meanQueueWait':statistics.mean(all_waits),'makespan':max(times)-min(arrivals)},'stages':reports,'jobs':[{'id':i,'arrived':a,'completed':b,'cycle':b-a,'queueWait':w} for i,(a,b,w) in enumerate(zip(arrivals,times,all_waits))]}

def analyze(data):
    n=data.get('jobs',200);interval=float(data.get('arrivalMean',5));seed=data.get('seed',42)
    if not isinstance(n,int) or not 1<=n<=10000:raise ValueError('jobs must be between 1 and 10000')
    if not math.isfinite(interval) or interval<=0:raise ValueError('arrivalMean must be positive and finite')
    if not data.get('stages'):raise ValueError('Provide at least one stage')
    mode=data.get('arrivalDistribution','constant')
    if mode not in ['constant','exponential']:raise ValueError('Unsupported arrival distribution')
    rng=random.Random(seed);arrivals=[0.]
    for _ in range(n-1):arrivals.append(arrivals[-1]+(interval if mode=='constant' else rng.expovariate(1/interval)))
    base=simulate(arrivals,data['stages'],seed);result={'product':'WorkflowLab','version':'0.1.0',**base,'findings':[]}
    if data.get('scenario'):
        other=simulate(arrivals,data['scenario'],seed);result['scenario']=other;result['comparison']={k:{'baseline':base['summary'][k],'scenario':other['summary'][k],'delta':other['summary'][k]-base['summary'][k]} for k in ['meanCycle','p95Cycle','meanQueueWait','makespan']}
    result['limitations']=['Synthetic model, not a forecast of actual business performance.','Time units are user-defined but must be consistent. No abandonment, rework, routing branches, shifts or downstream blocking.','Single finite run from an empty system; no steady-state confidence intervals.','Shared arrivals and seed support reproducibility; changed stage structures can consume random draws differently.']
    return result
