import config
import logic
import multiprocessing
from datetime import datetime

def main():
    queue = multiprocessing.JoinableQueue()

    procs = []
    for i in xrange(config.threads):
        procs.append(multiprocessing.Process(target=logic.worker, args=(queue,)))
        procs[-1].daemon = True
        procs[-1].start()

    start = datetime.now()
    print "DB build started on {}.".format(start)

    fathers = logic.build_db().keys()
    for item in fathers:
        if not 'Upsilon' in item:
            queue.put(item)

    queue.join()

    for p in procs:
      queue.put( None )
    queue.join()

    for p in procs:
        p.join()

    end = datetime.now()

    print "Took {} to build!".format(end - start)
    print "Active children:", multiprocessing.active_children()



if __name__ == '__main__':
    main()