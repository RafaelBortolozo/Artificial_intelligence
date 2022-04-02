const initialCombination = [3,3,1,0,0,0] //missionarios_left, canibais_left, missionarios_right, canibais_right
const finalCombination = [0,0,0,3,3,1]
let combinationHistory = [initialCombination]

const combinationsBoat = [
    [1,0],
    [2,0],
    [1,1],
    [0,1],
    [0,2]
]

function createNode(combination){
    return {
        combination,
        children: []
    }
}

function decimalDistance(init, end){
    //transforma a combinação em array para uma string binaria
    function convertArrayInBinaryString(array){ 
        let str = ''
        for(let i of array){
            for(let j=0 ; j<3 ; j++){
                if(i > 0){
                    i -= 1
                    str += '1'
                } else {
                    str += '0'
                }
            }
        }
        return str
    }

    init = convertArrayInBinaryString(init)
    end = convertArrayInBinaryString(end)

    let count = parseInt(init, 2) + parseInt(end, 2)

    return count
}

function validatePossibility(possibility){
    //verificar numero de missionarios e canibais (ignorando o lado do barco)
    for(let value of possibility){
        if(value < 0 || value > 3) return false
    }

    //verificar se a combinação já foi analisada
    let analyzedCombination = combinationHistory.some(item => {
        return item.toString() == possibility.toString()
    })
    if(analyzedCombination) return false
    
    //verificar se há mais canibais que missionarios, a condicional é invalida caso não há missionarios naquele lado
    if(
        (possibility[0] < possibility[1] && possibility[0] != 0) || 
        (possibility[3] < possibility[4] && possibility[3] != 0)){ 
        return false
    }else{
        return true
    }
}

function getValidPossibilities(node){
    let newValidPossibilities = [] //array de novas possibilidades validas
    let possibility = []
    for(let combinationBoat of combinationsBoat){ //para cada combinação de barco...
        if (node.combination[2] == 1) { // se barco estar a esquerda, remove pessoas da esquerda e joga pra direita ou então o inverso
            possibility = [ 
                node.combination[0] - combinationBoat[0],
                node.combination[1] - combinationBoat[1],
                0,
                node.combination[3] + combinationBoat[0],
                node.combination[4] + combinationBoat[1],
                1
            ]
        } else {
            possibility = [ 
                node.combination[0] + combinationBoat[0],
                node.combination[1] + combinationBoat[1],
                1,
                node.combination[3] - combinationBoat[0],
                node.combination[4] - combinationBoat[1],
                0
            ]
        }
        //verificar possibilidade
        if(validatePossibility(possibility)){ 
            newValidPossibilities.push(possibility)
        } 
    }

    return newValidPossibilities
}

function isDifferent(array1, array2){
    if(array1.toString() != array2.toString()) return true

    return false
}

function createSearchATree(rootState) {
    //inicialmente cria uma raiz da arvore, é o estado inicial do problema
    if(rootState == null){ 
        rootState = createNode(initialCombination)
    }

    //enquanto não atingir a combinação final...
    if (isDifferent(rootState.combination, finalCombination)) { 
        //coletar novas combinações validas
        let children = getValidPossibilities(rootState) 

        //para cada combinação, cria um novo nodo e adiciona-o como filho do nodo raiz
        for (let child of children) { 
            rootState.children.push(createNode(child))
        }

        let distances = []
        for (let child of rootState.children) {
            let distanceCurrentNext = decimalDistance(rootState.combination, child.combination)
            let distanceNextFinal = decimalDistance(child.combination, finalCombination)
            let distanceTotal = distanceCurrentNext + distanceNextFinal
            distances.push(distanceTotal)
        }

        //achar valor mais proximo do destino (menor)
        let min = Math.min(...distances)
        let bestIndex = distances.indexOf(min)

        //recursividade usando o melhor nodo filho
        let newRoot = rootState.children[bestIndex]
        combinationHistory.push(newRoot.combination)
        rootState.children.push(createSearchATree(newRoot))
    } 

    return rootState
}

let root = createSearchATree(null);
//console.log(root)
console.log(combinationHistory)