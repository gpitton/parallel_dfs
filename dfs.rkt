#lang racket/base
;; Run a depth-first search on the power set of S,
;; starting from the subset s0 and including elements of S.
;; It excludes from the search all the subsets of S that are
;; subsets of any of the elements in E (E for exclude).
;; For the time being, S is assumed to be a set of integers.


(require racket/format
         racket/list
         racket/set
         racket/string)


;; This function executes the looping over the subsets obtained by
;; adding to s0 the n-th element of S.
(define (dfs-adj s0 S marked n)
  (if (>= n (length S)) marked
      (let* ((i (list-ref S n))
             (sn (set-add s0 i))
             (seen (set-member? marked sn))
             (mk (dfs-adj s0 S marked (add1 n))))
        (if seen
            (set-union mk marked)
            (set-union mk (dfs sn (remove i S) (set-add marked sn)))))))
 


(define (dfs s0 S marked)
  (if (null? S) marked
      (let ((mk (dfs-adj s0 S (set-add marked s0) 0)))
        (set-union mk marked))))
      


;; Converts a string of comma-separated integers to a list of numbers.
(define (parse-stringnum s)
  (map string->number (string-split s ",")))


;; Parse command line arguments. It assumes that s0 is passed through a flag "-s0",
;; and that S is passed through a flag "-S".
(define (parse-args args)
  (cond ((null? args) '())
        ((or (string=? (car args) "-s0")
             (string=? (car args) "-S"))
         (cons (parse-stringnum (cadr args))
               (parse-args (cddr args))))
        (else (error "Wrong command line arguments."))))


;; Generates a string for pretty-printing a set of integers.
(define (str-set s)
  (define (str-set-aux x)
    (if (set-empty? x) ""
        (string-append ","
                       (~a (set-first x))
                       (str-set-aux (set-rest x)))))
  ;; We need to remove the first comma.
  (string-append "{" (substring (str-set-aux s) 1) "}"))


(define (main)
  (let* ((args (parse-args (vector->list (current-command-line-arguments))))
         (s0 (car args))
         (Idxs (cadr args))
         (S (for/set
                [(i Idxs)
                #:unless (member i s0)]
              i)))
    (dfs (list->set s0) S)))


;(main)
(define subsets (dfs (set 1) (range 1 9) (set (set 1))))
(for [(s (in-set subsets))]
  (printf "~a~n" (str-set s)))
(displayln (set-count subsets))
