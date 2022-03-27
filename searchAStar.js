const initialCombination = [3,3,0,0]
const finalCombination = [0,0,3,3]
let root = null

const combinationsBoat = [
    [1,0],
    [2,0],
    [1,1],
    [0,1],
    [0,2]
]

function createNode(combination, boatSide){
    return {
        combination,
        boatSide,
        children: []
    }
}

function hammingDistance(init, end){
    function convertArrayInBinaryString(array){ //transforma a combinação em array para uma string binaria, aumentando a precisão da distancia de Hamming
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

    init = convertArrayInBinaryString(init).split('') //split na string para comparar caracteres
    end = convertArrayInBinaryString(end).split('')

    let count = 0
    for(let i in end){ //contagem de caracteres diferentes
        if(init[i] != end[i]) count++
    }
    
    return count
}

function validatePossibility(possibility){
    //verificar se há mais canibais que missionarios, a condicional é invalida caso não há missionarios naquele lado
    if( (possibility[0] < possibility[1] && possibility[0] > 0) || 
        (possibility[2] < possibility[3] && possibility[2] > 0)){ 
        return false
    }else{
        return true
    }
}

function getValidPossibilities(node){
    let newValidPossibilities = [] //array de novas possibilidades validas
    let possibility = []
    for(let combinationBoat of combinationsBoat){ //para cada combinação de barco...
        if (node.boatSide === 'left') { // se barco estar a esquerda, remove pessoas da esquerda e joga pra direita ou então o inverso
            possibility = [ 
                node.combination[0] - combinationBoat[0],
                node.combination[1] - combinationBoat[1],
                node.combination[2] + combinationBoat[0],
                node.combination[3] + combinationBoat[1]
            ]
        } else {
            possibility = [ 
                node.combination[0] + combinationBoat[0],
                node.combination[1] + combinationBoat[1],
                node.combination[2] - combinationBoat[0],
                node.combination[3] - combinationBoat[1]
            ]
        }
        
        if(validatePossibility(possibility)){ //verificar possibilidade
            newValidPossibilities.push(possibility)
        } 
    }

    return newValidPossibilities
}

function createSearchATree(rootState) {
    if(rootState == null){ //inicialmente cria uma raiz da arvore, é o estado inicial do problema
        rootState = createNode(initialCombination, 'left')
    }
    
    if (rootState.combination != finalCombination) { //enquanto não atingir a combinação final...
        let children = getValidPossibilities(rootState) //coletar novas combinações validas
        for (let child of children) { //para cada combinação, cria um novo nodo e adiciona-o como filho do nodo raiz
            if (rootState.boatSide == 'left') {
                rootState.children.push(createNode(child, 'right'))
            } else {
                rootState.children.push(createNode(child, 'left'))
            }
        }

        // Calcular distancia distancias
        // Formula: distancia entre o ponto atual e o próximo + distancia do próximo ponto até o destino
        let distances = []
        for (let child of rootState.children) {
            let distanceCurrentNext = hammingDistance(rootState.combination, child.combination)
            let distanceNextFinal = hammingDistance(child.combination, finalCombination)
            let distanceTotal = distanceCurrentNext + distanceNextFinal
            distances.push(distanceTotal)
        }

        //achar valor mais proximo do destino (menor)
        let min = Math.min(...distances)
        let bestIndex = distances.indexOf(min)

        rootState = createSearchATree(rootState.children[bestIndex])
    } 

    return rootState
}

// console.log(binary.decimal(1010))
root = createSearchATree(root);
console.log(root)




//createNode(currentState.combination, currentState.boatSide)



// function checkMoreCannibals(side){
//     if(side[0] < side[1]) return true
// }

// createPoints(currentState)

// const inicio = {
//     children: [],
//     distanceInicial: 0,
//     state: [3,3,1,0,0,0]
//    }
   
//    const final = {
//     parent: null,
//     children: [],
//     state: [0,0,0,3,3,1]
//    }
   
//    const possibleActions = [
//      [1,1],
//      [0,1],
//      [1,0],
//      [2,0],
//      [0,2],
//    ]
   
//    let visitedNode = []
//    let result
//    let prof = 0
   
//    function transform(e){
//      if(e == 0){
//        return '000'
//      }else if(e == 1) {
//        return '001'
//      }else if(e == 2) {
//        return '011'
//      }else if(e == 3) {
//        return '111'
//      }
//    }
   
//    function hammingDistance(a, b) {
//      let distance = 0
   
//      const newA = `${transform(a[0]) + transform(a[1]) + transform(a[3]) + transform(a[4])}`
//      const newB = `${transform(b[0]) + transform(b[1]) + transform(b[3]) + transform(b[4])}`
   
//      for (let i = 0; i < newA.length; i += 1) {
//        if (newA[i] !== newB[i]) {
//          distance += 1
//        }
//      }
    
//      return distance;
//    }
   
//    function validState(currentState){ 
//      if(visitedNode.includes(currentState.toString())) return false
   
//      if((currentState[0] < currentState[1] && currentState[0] != 0) || (currentState[3] < currentState[4] && currentState[3] != 0)) return false
   
//      return true
//    }
   
//    function nextState(currentState, next){
//      const newState = (currentState.state[2] == 1) ? [ //Se o barco estar a esquerda (representado pelo 1), então cria 
//            currentState.state[0] - next[0],            //um novo array de missionarios-canibais usando cada combinacao daquele array de possibilidades
//            currentState.state[1] - next[1],            // Nesta primeira condicional, está removendo as pessoas da esquerda e jogando para a direita
//            0, 
//            currentState.state[3] + next[0], 
//            currentState.state[4] + next[1], 
//            1
//          ] 
//          :  [
//              currentState.state[0] + next[0], 
//              currentState.state[1] + next[1], 
//              1, 
//              currentState.state[3] - next[0], 
//              currentState.state[4] - next[1], 
//              0
//          ]
    
//      const inicial = currentState.distanceInicial + hammingDistance(currentState.state, newState) //
//      const nextNode = {
//        parent: currentState,
//        distanceInicial: inicial,
//        totalDistance: inicial + hammingDistance(newState, final.state),
//        state: newState,
//        children: []
//      }
   
//      if(validState(nextNode.state)) currentState.children.push(nextNode)
//      return currentState 
//    }
   
//    function print(finalState){
//      result = `${finalState.state[0]}m ${finalState.state[1]}c ${finalState.state[2] == 1 ? ' \uD83D\uDEF6....... ' : ' .......\uD83D\uDEF6 '} ${finalState.state[3]}m ${finalState.state[4]}c \n` + (result || '')
   
//      if(!finalState.parent) return console.log(`Resultado da busca (profundidade ${prof}) \n\n` + result)
     
//      prof++
//      print(finalState.parent)
//    }
   
//    function createNode(node){
//      let actions = node; //copia do estado inicial
   
//      possibleActions.forEach(p => {
//        actions = nextState(actions, p)
//      })
   
//      const next = actions.children.reduce((a, b) => {
//        if(b.totalDistance <= a.totalDistance) a = b
//        return a
//      })
   
//      visitedNode.push(next.state.toString())
   
//      if(next.state.toString() == final.state.toString()) return print(next)
    
//      return createNode(next)
//    }
   
//    createNode(inicio)