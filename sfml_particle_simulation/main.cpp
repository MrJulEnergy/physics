#include <SFML/Graphics.hpp>
#include <vector>
#include <random>
#include <iostream>
#include <cmath>
//______________________________________


class Particle{

public:
    sf::CircleShape s;
    sf::Vector2f pos;
    sf::Vector2f vel;
    sf::Vector2f force;
    float mass;
    Particle(sf::Vector2f position, sf::Vector2f velocity, std::vector<int> color, int rad){
        pos = position;
        vel = velocity;

        s.setPosition(pos);
        s.setFillColor(sf::Color(color[0], color[1], color[2], color[3]));
        s.setRadius(rad);
        mass = rad;
    }; 
    void render(sf::RenderWindow& window){
        s.setPosition(pos);
        window.draw(s);
    };
    sf::Vector2f get_pos(){
        return pos;
    }; 
};
//____________________________________
float vecLen(sf::Vector2f a){
    float len = sqrt(a.x*a.x + a.y*a.y);
    return len;
}
//______________________________________
void zeroForces(std::vector<Particle>& particles){//nicht kaputt
    for(Particle& p: particles){
        sf::Vector2f zero(0, 0);
        p.force = zero; 
    }
}
//_____________________________________
std::vector<sf::Vector2f> forEachPair(const std::vector<Particle> particles){
    int len = particles.size();
    std::vector<sf::Vector2f> pairs;
    for(int i=0; i<=len-1; i++){
        for(int k=i+1; k<=len-1; k++){
            sf::Vector2f pair(i, k);
            pairs.push_back(pair);
        }
    } 
    return pairs;
}

//____________________________________
sf::Vector2f vecDis(Particle a, Particle b){
    sf::Vector2f dis = a.pos-b.pos;
    return dis;
}
//_____________________________________
float forceField(float dis){
    float force = -1/(dis);
    return force;
}
//_____________________________________
void calcForces(std::vector<Particle>& part){
    //make Pairs
    std::vector<sf::Vector2f> pairs = forEachPair(part);
    //distance
    for(sf::Vector2f& pair: pairs){
        sf::Vector2f vectorDis = vecDis(part[pair.x], part[pair.y]);
        float absDis = vecLen(vectorDis);
        //F = (1/r^2)ê_r
        float force = forceField(absDis);
        //unit_vec
        sf::Vector2f unitVec = (1/absDis) * vectorDis; 
        part[pair.x].force += force * unitVec;
        part[pair.y].force += - force * unitVec;
    }
}
//_____________________________________
void propVelPos(std::vector<Particle>& particles, float dt){
    for(Particle& p: particles){
        p.vel += (1/p.mass)*3000*dt*p.force;
        p.pos += dt*p.vel;
    }
}
//______________________________________
void updatePhysics(std::vector<Particle>& particles, float dt){    
    //Force = 0 
    zeroForces(particles);
    //F += forces
    calcForces(particles);   
    // v+= F*dt/m
    // x += v*dt
    propVelPos(particles, dt);
}

//______________________________________
int randInt(int min, int max){
    std::random_device rd;
    std::mt19937 rng(rd());
    std::uniform_int_distribution<int> uni(min, max);

    int v = uni(rng);
    return v;
}

sf::Vector2f randVec(int min_a, int max_a, int min_b, int max_b){
    sf::Vector2f v(randInt(min_a, max_a), randInt(min_b, max_b));
    return v;
}

//______________________________________

int main(){
    sf::RenderWindow window(sf::VideoMode(1000, 1000), "Project 3");
    window.setFramerateLimit(100);

    int n = 250;
    std::vector<Particle> particles;
    particles.clear();
    for(int i=0; i<=n; i++){
        sf::Vector2f pos = randVec(0, 1000, 0, 1000);
        sf::Vector2f vel= randVec(-50, 50, -50, 50);
        sf::Vector2f zero(0, 0);
        sf::Vector2f col = randVec(20, 255, 20, 255);
        sf::Vector2f col2 = randVec(20, 255, 20, 255);
        int r = randInt(2, 12);
        std::vector<int> color;
        color.push_back(col.x);
        color.push_back(col.y);
        color.push_back(col2.x);
        color.push_back(col2.y);
        particles.push_back(Particle(pos, vel, color, r));
    }

    sf::Clock clock;
    while(window.isOpen()){
        sf::Event event;
        float dt = clock.restart().asSeconds();

        while(window.pollEvent(event)){
            if(event.type == sf::Event::Closed) window.close();
            if(sf::Keyboard::isKeyPressed(sf::Keyboard::Escape)) window.close();
        }
        window.clear();
        for(Particle p: particles){
            p.render(window);
        }
        updatePhysics(particles, dt);
        window.display();
    }
    return 0;
}
//______________________________________


